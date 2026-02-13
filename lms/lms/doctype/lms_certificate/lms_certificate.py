# Copyright (c) 2021, FOSS United and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.email.doctype.email_template.email_template import get_email_template
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import add_years, nowdate, getdate
from lms.lms.utils import is_certified


class LMSCertificate(Document):
    def validate(self):
        self.validate_duplicate_certificate()

    def autoname(self):
        self.name = make_autoname("hash", self.doctype)

    def after_insert(self):
        if not frappe.flags.in_test:
            outgoing_email_account = frappe.get_cached_value(
                "Email Account", {"default_outgoing": 1,
                                  "enable_outgoing": 1}, "name"
            )
            if outgoing_email_account or frappe.conf.get("mail_login"):
                self.send_mail()

    def send_mail(self):
        subject = _("Congratulations on getting certified!")
        template = "certification"
        custom_template = frappe.db.get_single_value(
            "LMS Settings", "certification_template")

        args = {
            "student_name": self.member_name,
            "course_name": self.course,
            "course_title": frappe.db.get_value("LMS Course", self.course, "title"),
            "certificate_name": self.name,
            "template": self.template,
        }

        if custom_template:
            email_template = get_email_template(custom_template, args)
            subject = email_template.get("subject")
            content = email_template.get("message")
        frappe.sendmail(
            recipients=self.member,
            subject=subject,
            template=template if not custom_template else None,
            content=content if custom_template else None,
            args=args,
            header=[subject, "green"],
        )

    def validate_duplicate_certificate(self):
        self.validate_course_duplicates()
        self.validate_batch_duplicates()

    def validate_course_duplicates(self):
        if self.course:
            course_duplicates = frappe.get_all(
                "LMS Certificate",
                filters={
                    "member": self.member,
                    "name": ["!=", self.name],
                    "course": self.course,
                },
                fields=["name", "course", "course_title"],
            )
            if len(course_duplicates):
                full_name = frappe.db.get_value(
                    "User", self.member, "full_name")
                frappe.throw(
                    _("{0} is already certified for the course {1}").format(
                        full_name, course_duplicates[0].course_title
                    )
                )

    def validate_batch_duplicates(self):
        if self.batch_name:
            batch_duplicates = frappe.get_all(
                "LMS Certificate",
                filters={
                    "member": self.member,
                    "name": ["!=", self.name],
                    "batch_name": self.batch_name,
                },
                fields=["name", "batch_name", "batch_title"],
            )
            if len(batch_duplicates):
                full_name = frappe.db.get_value(
                    "User", self.member, "full_name")
                frappe.throw(
                    _("{0} is already certified for the batch {1}").format(
                        full_name, batch_duplicates[0].batch_title
                    )
                )

    def on_update(self):
        frappe.share.add_docshare(
            self.doctype,
            self.name,
            self.member,
            write=1,
            share=1,
            flags={"ignore_share_permission": True},
        )


def has_website_permission(doc, ptype, user, verbose=False):
    if ptype in ["read", "print"]:
        return True
    if doc.member == user and ptype == "create":
        return True
    return False


def send_expiry_notifications():
    # Ambil semua certificate yang sudah expired (dan punya expiry_date)
    certs = frappe.get_all(
        "LMS Certificate",
        filters={
            "expiry_date": ["<=", getdate(nowdate())]
        },
        fields=["name", "member", "course", "course_title", "expiry_date"]
    )

    notif = frappe.get_doc("Notification", "Certificate Expired (student)")

    for c in certs:
        # Skip jika expiry_date kosong (artinya lifetime)
        if not c.expiry_date:
            continue

        # Kirim notifikasi
        doc = frappe.get_doc("LMS Certificate", c.name)
        notif.send(doc)

        # Cari enrollment student untuk course terkait
        enrollment = frappe.get_all(
            "LMS Enrollment",
            filters={
                "member": c.member,
                "course": c.course
            },
            fields=["name", "progress"]
        )

        if enrollment:
            enrollment_doc = frappe.get_doc(
                "LMS Enrollment", enrollment[0].name)

            # Reset progress ke 0 jika sebelumnya tidak 0
            if enrollment_doc.progress > 0:
                enrollment_doc.progress = 0
                enrollment_doc.save(ignore_permissions=True)

                frappe.logger("lms").info(
                    f"[CERTIFICATE EXPIRED] Reset progress for member {c.member} in course {c.course}"
                )

            # Hapus record progress di "LMS Course Progress"
            course_progress_records = frappe.get_all(
                "LMS Course Progress",
                filters={
                    "member": c.member,
                    "course": c.course
                },
                pluck="name"
            )

            for rec in course_progress_records:
                frappe.delete_doc("LMS Course Progress", rec,
                                  ignore_permissions=True)
                frappe.logger("lms").info(
                    f"Deleted course progress record {rec} for {c.member} in {c.course}"
                )

    frappe.db.commit()


@frappe.whitelist()
def create_certificate(course):
    # Cek apakah user sudah punya sertifikat untuk course ini
    certificate_name = is_certified(course)

    # Ambil masa berlaku dari course (Select field)
    validity = frappe.db.get_value(
        "LMS Course", course, "certificate_validity")

    issue_date = nowdate()
    expiry_date = None

    # Tentukan expiry date berdasarkan pilihan
    if validity and validity != "Lifetime":
        years = 0
        if "1 Year" in validity:
            years = 1
        elif "2 Year" in validity:
            years = 2
        elif "3 Year" in validity:
            years = 3

        if years > 0:
            expiry_date = add_years(issue_date, years)

    # Jika sudah ada certificate, update expiry_date saja
    if certificate_name:
        cert_doc = frappe.get_doc("LMS Certificate", certificate_name)

        # Update expiry_date berdasarkan validity baru
        cert_doc.expiry_date = expiry_date
        cert_doc.issue_date = issue_date
        cert_doc.save(ignore_permissions=True)

        frappe.logger("lms").info(
            f"Updated certificate {cert_doc.name} expiry_date to {expiry_date}"
        )

        return frappe.db.get_value(
            "LMS Certificate",
            cert_doc.name,
            ["name", "course", "template", "expiry_date"],
            as_dict=True,
        )

    # Jika belum ada certificate, ambil template default
    default_certificate_template = frappe.db.get_value(
        "Property Setter",
        {"doc_type": "LMS Certificate", "property": "default_print_format"},
        "value",
    )
    if not default_certificate_template:
        default_certificate_template = frappe.db.get_value(
            "Print Format", {"doc_type": "LMS Certificate"}, "name"
        )

    # Buat dokumen certificate baru
    cert_doc = frappe.get_doc(
        {
            "doctype": "LMS Certificate",
            "member": frappe.session.user,
            "course": course,
            "issue_date": issue_date,
            "expiry_date": expiry_date,
            "template": default_certificate_template,
            "published": 1
        }
    )
    cert_doc.save(ignore_permissions=True)

    frappe.logger("lms").info(
        f"Created new certificate {cert_doc.name} for course {course} (expiry: {expiry_date})"
    )

    return cert_doc
