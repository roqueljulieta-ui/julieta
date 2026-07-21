import requests
import os
from datetime import datetime

BUSINESS_EMAIL = "info@servicestrucks.com"
WHATSAPP_NUMBER = "34661388880"
BACKEND_URL = "https://servicestrucks-backend.onrender.com"

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
RESEND_FROM = "Services Truck <info@servicestrucks.com>"


def _send_email(subject, html_body, to_email):
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": "Bearer " + RESEND_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "from": RESEND_FROM,
                "to": [to_email],
                "subject": subject,
                "html": html_body,
            },
            timeout=10,
        )
        if response.status_code >= 400:
            print("[EMAIL ERROR] " + response.text)
            return {"success": False, "error": response.text}

        print("[EMAIL] Sent successfully to " + to_email)
        return {"success": True, "message": "Email sent"}
    except Exception as e:
        print("[EMAIL ERROR] " + str(e))
        return {"success": False, "error": str(e)}


def send_contact_email(data):
    nombre = data.get("nombre", "")
    email = data.get("email", "")
    telefono = data.get("telefono", "")
    mensaje = data.get("mensaje", "")
    fecha = datetime.now().strftime("%d/%m/%Y a las %H:%M")

    subject = "Nuevo Mensaje de Contacto - " + nombre

    html_body = ("""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #0A1929; border-bottom: 3px solid #FF6B00; padding-bottom: 10px;">
                    Nuevo Mensaje de Contacto
                </h2>
                <div style="margin: 20px 0;">
                    <p><strong>Nombre:</strong> """ + nombre + """</p>
                    <p><strong>Email:</strong> """ + email + """</p>
                    <p><strong>Telefono:</strong> """ + telefono + """</p>
                    <p><strong>Mensaje:</strong></p>
                    <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
                        """ + mensaje + """
                    </div>
                    <p style="color: #666; font-size: 12px; margin-top: 20px;">
                        Recibido el """ + fecha + """
                    </p>
                </div>
            </div>
        </body>
    </html>
    """)
    return _send_email(subject, html_body, BUSINESS_EMAIL)


def send_appointment_email(data, appointment_id):
    """Notifica al negocio con un boton para confirmar la cita"""
    nombre = data.get("nombre", "")
    apellidos = data.get("apellidos", "")
    email = data.get("email", "")
    telefono = data.get("telefono", "")
    fecha_preferida = data.get("fecha_preferida", "")
    hora_preferida = data.get("hora_preferida", "")
    tipo_servicio = data.get("tipo_servicio", "")
    descripcion = data.get("descripcion", "")
    fecha = datetime.now().strftime("%d/%m/%Y a las %H:%M")

    confirm_link = BACKEND_URL + "/api/appointments/" + appointment_id + "/confirm"

    subject = "Nueva Solicitud de Cita - " + nombre + " " + apellidos

    html_body = ("""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #0A1929; border-bottom: 3px solid #FF6B00; padding-bottom: 10px;">
                    Nueva Solicitud de Cita
                </h2>
                <div style="margin: 20px 0;">
                    <h3 style="color: #FF6B00;">Datos del Cliente:</h3>
                    <p><strong>Nombre Completo:</strong> """ + nombre + " " + apellidos + """</p>
                    <p><strong>Email:</strong> """ + email + """</p>
                    <p><strong>Telefono:</strong> """ + telefono + """</p>

                    <h3 style="color: #FF6B00; margin-top: 20px;">Detalles de la Cita:</h3>
                    <p><strong>Fecha Preferida:</strong> """ + fecha_preferida + """</p>
                    <p><strong>Hora Preferida:</strong> """ + hora_preferida + """</p>
                    <p><strong>Tipo de Servicio:</strong> """ + tipo_servicio + """</p>

                    <p><strong>Descripcion:</strong></p>
                    <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
                        """ + descripcion + """
                    </div>

                    <div style="margin-top: 30px; text-align: center;">
                        <a href='""" + confirm_link + """' style="background: #FF6B00; color: #ffffff; text-decoration: none; padding: 14px 28px; border-radius: 6px; font-weight: bold; display: inline-block;">
                            Confirmar Cita
                        </a>
                    </div>

                    <p style="color: #666; font-size: 12px; margin-top: 20px;">
                        Recibido el """ + fecha + """
                    </p>
                </div>
            </div>
        </body>
    </html>
    """)
    return _send_email(subject, html_body, BUSINESS_EMAIL)


def send_appointment_received_email(data):
    """Se envia al cliente automaticamente unos minutos despues de enviar el formulario"""
    nombre = data.get("nombre", "")
    email = data.get("email", "")
    tipo_servicio = data.get("tipo_servicio", "")
    fecha_preferida = data.get("fecha_preferida", "")
    hora_preferida = data.get("hora_preferida", "")

    subject = "Hemos recibido tu solicitud - Services Trucks"

    html_body = ("""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #0A1929; border-bottom: 3px solid #FF6B00; padding-bottom: 10px;">
                    Hemos recibido tu solicitud
                </h2>
                <div style="margin: 20px 0;">
                    <p>Hola """ + nombre + """,</p>
                    <p>Gracias por contactar a <strong>Services Trucks Mecanica Pesada</strong>.</p>
                    <p>Hemos recibido tu solicitud para <strong>""" + tipo_servicio + """</strong> el dia """ + fecha_preferida + """ a las """ + hora_preferida + """.</p>
                    <p>En breve nos pondremos en contacto contigo para confirmar los detalles.</p>
                    <p style="margin-top: 30px;">Un saludo,<br/>Equipo Services Trucks</p>
                </div>
            </div>
        </body>
    </html>
    """)
    return _send_email(subject, html_body, email)


def send_appointment_confirmed_email(data):
    """Se envia al cliente cuando el negocio confirma la cita"""
    nombre = data.get("nombre", "")
    email = data.get("email", "")
    tipo_servicio = data.get("tipo_servicio", "")
    fecha_preferida = data.get("fecha_preferida", "")
    hora_preferida = data.get("hora_preferida", "")

    subject = "Tu cita ha sido confirmada - Services Trucks"

    html_body = ("""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #0A1929; border-bottom: 3px solid #FF6B00; padding-bottom: 10px;">
                    Tu cita ha sido confirmada
                </h2>
                <div style="margin: 20px 0;">
                    <p>Hola """ + nombre + """,</p>
                    <p>Te confirmamos tu cita para <strong>""" + tipo_servicio + """</strong> el dia """ + fecha_preferida + """ a las """ + hora_preferida + """.</p>
                    <p>Si necesitas modificar el horario, responde a este correo o escribenos por WhatsApp.</p>
                    <p style="margin-top: 30px;">Un saludo,<br/>Equipo Services Trucks</p>
                </div>
            </div>
        </body>
    </html>
    """)
    return _send_email(subject, html_body, email)


def generate_whatsapp_link(data, message_type="contact"):
    try:
        import urllib.parse
        if message_type == "appointment":
            nombre = data.get("nombre", "")
            apellidos = data.get("apellidos", "")
            fecha_preferida = data.get("fecha_preferida", "")
            hora_preferida = data.get("hora_preferida", "")
            tipo_servicio = data.get("tipo_servicio", "")
            descripcion = data.get("descripcion", "")
            message = (
                "Hola, me gustaria confirmar mi solicitud de cita:\n\n"
                + nombre + " " + apellidos + "\n"
                + fecha_preferida + " a las " + hora_preferida + "\n"
                + "Servicio: " + tipo_servicio + "\n"
                + descripcion + "\n\n"
                + "Podemos confirmar la cita?"
            )
        else:
            nombre = data.get("nombre", "")
            mensaje = data.get("mensaje", "")
            message = (
                "Hola, acabo de enviar un mensaje desde la web:\n\n"
                + mensaje + "\n\nSaludos,\n" + nombre
            )

        encoded_message = urllib.parse.quote(message)
        whatsapp_url = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encoded_message
        print("[WHATSAPP] Generated link for " + str(data.get("nombre", "Unknown")))
        return whatsapp_url
    except Exception as e:
        print("[WHATSAPP ERROR] " + str(e))
        return "https://wa.me/" + WHATSAPP_NUMBER
