import frappe


def create_enrollment_history(doc, method):
    frappe.get_doc({
        "doctype": "LMS Enrollment History",
        "enrollment": doc.name,
        "member": doc.member,
        "course": doc.course,
        "action": "Enroll",
        "date": frappe.utils.now(),
    }).insert(ignore_permissions=True)
