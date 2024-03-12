from django.core.mail import send_mail   
from django.conf import settings

def enviarCorreo(asunto, mensaje, email):
    subject = asunto
    message = mensaje
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list)