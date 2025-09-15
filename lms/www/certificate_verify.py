import frappe


def get_context(context):
    context.no_cache = 1
    certificate_id = frappe.form_dict.certificate_id

    if not certificate_id:
        context.certificate = None
        context.certificate_id = None
        context.iframe_url = None
        return context

    try:
        certificate = frappe.get_doc("LMS Certificate", certificate_id)
    except frappe.DoesNotExistError:
        context.certificate = None
        context.certificate_id = certificate_id
        context.iframe_url = None
        return context

    context.certificate = certificate
    context.certificate_id = certificate_id
    # Gunakan print format sesuai field template pada dokumen certificate
    print_format = getattr(certificate, 'template', None) or 'Standard'
    # Gunakan endpoint API download_pdf langsung
    context.iframe_url = f"/api/method/frappe.utils.print_format.download_pdf?doctype=LMS Certificate&name={certificate_id}&format={print_format}&letterhead=None&no_letterhead=0&_lang=en&key=None"
    context.title = f"Certificate Verification - {certificate_id}"
    return context
