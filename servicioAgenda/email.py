from django.core.mail import send_mail   
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from servicioAgenda.authentication import generar_token_recuperacion



def enviarCorreoRecuperacion(email,id_usuario):
    token = generar_token_recuperacion(email,id_usuario)
    url_recuperacion = f"http://localhost:5173/recuperar-contrasena?token={token}"
    mensaje = f"Hola, has solicitado recuperar tu contraseña, por favor usa el siguiente enlace para restablecerla (expira en 1 hora): {url_recuperacion}\nSi no fuiste tú, ignora este mensaje."
    asunto = "Recuperación de contraseña"
    enviarCorreo(mensaje, asunto, email)

def enviarCorreo(mensaje, asunto, email):
    subject = asunto
    message = mensaje
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)