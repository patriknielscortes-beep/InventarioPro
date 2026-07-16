import os
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

EMAIL = os.getenv("MAIL_EMAIL")
PASSWORD = os.getenv("MAIL_PASSWORD")


def enviar_boleta(destinatario, nombre_cliente, folio, ruta_pdf):

    try:

        mensaje = EmailMessage()

        mensaje["Subject"] = f"PARTRICK | Boleta Electrónica Nº {folio}"

        mensaje["From"] = EMAIL

        mensaje["To"] = destinatario

        mensaje.set_content(
            f"""
Hola {nombre_cliente}.

Gracias por comprar en PARTRICK.

Adjuntamos su boleta electrónica.

Folio: {folio}

Saludos.
Equipo PARTRICK.
"""
        )

        with open(ruta_pdf, "rb") as archivo:

            mensaje.add_attachment(
                archivo.read(),
                maintype="application",
                subtype="pdf",
                filename=f"Boleta_{folio}.pdf"
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(EMAIL, PASSWORD)

            smtp.send_message(mensaje)

        return True

    except Exception as e:

        print("ERROR SMTP:", e)

    raise