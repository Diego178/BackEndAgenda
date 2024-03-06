from django.core.mail import send_mail   
from django.conf import settings

def enviarCorreo(username, email):
    subject = 'Se elimino la asesoria'
    message = f'Hola {username}, la asesoria que tenia para el jueves 24 de mayo se cancelo.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list)