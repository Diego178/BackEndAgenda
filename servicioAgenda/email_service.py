from mailersend import emails
from servicioAgenda.authentication import generar_token_recuperacion
from dotenv import load_dotenv
import os
load_dotenv()

def enviarCorreoRecuperacion(email,id_usuario, usuario):
    print('llega aqui')
    token = generar_token_recuperacion(email,id_usuario)
    url_recuperacion = f"https://front-end-agenda.vercel.app/recuperar-contrasena?token={token}"
    mensaje = f"Hola, has solicitado recuperar tu contraseña, por favor usa el siguiente enlace para restablecerla (expira en 1 hora): {url_recuperacion}\nSi no fuiste tú, ignora este mensaje."
    asunto = "Recuperación de contraseña"
    enviarCorreo(mensaje, asunto, email, usuario)

def enviarCorreo(mensaje, asunto, email_destinatario, usuario):
    print(mensaje, asunto, email_destinatario, usuario)
    api_key = os.environ.get('KEY_SMTP')
    print(os.environ.get('EMAIL_HOST_USER'))
    email = emails.NewEmail(api_key)
    mail_body = {}
    mail_from = {
        "name": "Centro Autoacceso Xalapa",
        "email": "MS_EuOrkT@trial-zr6ke4nqz334on12.mlsender.net"
    }
    recipients = [
        {
        "name": usuario,
        "email": email_destinatario,
    }
    ]
    personalization = [
        {
            "email": email_destinatario,
            "data": {
                "asunto": asunto,
                "cuerpo": mensaje
            }
        }
    ]

    email.set_mail_from(mail_from, mail_body)
    email.set_mail_to(recipients, mail_body)
    email.set_subject(asunto, mail_body)
    email.set_template(os.environ.get('ID_TEMPLATE'), mail_body)
    email.set_personalization(personalization, mail_body)

    # Enviar el correo
    try:
        response = email.send(mail_body)
        print("Correo enviado exitosamente")
        print(response)  # Puedes imprimir la respuesta para verificar detalles del envío
    except Exception as e:
        print(f"Error al enviar el correo: {e}")