from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_otp_email(email, domain_name, server_ip, associated_account, customer_id, domain_account, ssl_status, hosted_account, remark, expires):
    subject = "Expiry - Alert"
    template_path = 'email.html'
    context = {
        'domain_name': domain_name,
        'server_ip': server_ip,
        'associated_account': associated_account,
        'customer_id': customer_id,
        'domain_account': domain_account,
        'ssl_status': ssl_status,
        'hosted_account': hosted_account,
        'remark': remark,
        'expires': expires,
    }
    try:
        message = render_to_string(template_path, context)
        msg = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [email])
        msg.attach_alternative(message, "text/html")
        msg.send()
    except Exception as e:
        print("Error: unable to send email:", e)
        return False
    return True
