import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

BUSINESS_EMAIL = "info@servicestrucks.com"
WHATSAPP_NUMBER = "34661388880"

SMTP_SERVER = "smtp.hostinger.com"
SMTP_PORT = 465
SMTP_USER = os.environ.get("EMAIL_USER", "info@servicestrucks.com")
SMTP_PASSWORD = os.environ.get("EMAIL_PASSWORD")


def _send_email(subject: str, html_body: str, to_email: str = BUSINESS_EMAIL):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())

        print(f"[EMAIL] Sent successfully to {to_email}")
        return {"success": True, "message": "Email sent"}
    except Exception as e:
        print(f"[EMAIL ERROR] {str(e)}")
        return {"success": False, "error": str(e)}


def send_contact_email(data: dict):
    """Send contact form notification email"""
    subject = f"Nuevo Mensaje de Contacto - {data['nombre']}"
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #0A1929; border-bottom: 3px solid #FF6B00; padding-bottom: 10px;">
                    Nuevo Mensaje de Contacto
                </h2>
                <div style="margin: 20px 0;">
                    <p><strong>Nombre:</strong> {data['nombre']}</p>
                    <p><strong>Email:</strong> {data['email']}</p>
                    <p><strong>Teléfono:</strong> {data['telefono']}</p>
                    <p><strong>Mensaje:</strong></p>
                    <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
                        {data['mensaje']}
                    </div>
                    <p style="color: #666; font-size: 12px; margin-top: 20px;">
                        Recibido el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}
                    </p>
                </div>
            </div>
        </body>
    </html>
    """
    return _send_email(subject, html_body)


def send_appointment_email(data: dict):
    """Send appointment notification email"""
    subject = f"Nueva Solicitud de Cita - {data['nombre']} {data['apellidos']}"
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;
