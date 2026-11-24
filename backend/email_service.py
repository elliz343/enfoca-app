import os
import smtplib
from email.message import EmailMessage


def enviar_correo(destinatario: str, asunto: str, texto: str) -> None:
    mensaje = EmailMessage()
    mensaje["From"] = os.environ["SMTP_FROM"]
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(texto)

    with smtplib.SMTP(
        os.environ["SMTP_HOST"],
        int(os.environ["SMTP_PORT"]),
        timeout=15,
    ) as servidor:
        servidor.starttls()
        servidor.login(
            os.environ["SMTP_USERNAME"],
            os.environ["SMTP_PASSWORD"],
        )
        servidor.send_message(mensaje)
