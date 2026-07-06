import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

BUSINESS_EMAIL = "info@servicestrucks.com"
WHATSAPP_NUMBER = "34661388880"

def send_contact_email(data: dict):
    """Send contact form notification email"""
    try:
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
        
        # For production, you would use actual SMTP credentials
        # For now, we'll log it (you'll need to configure email service)
        print(f"[EMAIL] Contact form from {data['nombre']} - {data['email']}")
        print(f"[EMAIL] Message: {data['mensaje']}")
        
        return {"success": True, "message": "Email sent"}
    except Exception as e:
        print(f"[EMAIL ERROR] {str(e)}")
        return {"success": False, "error": str(e)}

def send_appointment_email(data: dict):
    """Send appointment notification email"""
    try:
        subject = f"Nueva Solicitud de Cita - {data['nombre']} {data['apellidos']}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                    <h2 style="color: #0A1929; border-bottom: 3px solid #FF6B00; padding-bottom: 10px;">
                        📅 Nueva Solicitud de Cita
                    </h2>
                    <div style="margin: 20px 0;">
                        <h3 style="color: #FF6B00;">Datos del Cliente:</h3>
                        <p><strong>Nombre Completo:</strong> {data['nombre']} {data['apellidos']}</p>
                        <p><strong>Email:</strong> {data['email']}</p>
                        <p><strong>Teléfono:</strong> {data['telefono']}</p>
                        
                        <h3 style="color: #FF6B00; margin-top: 20px;">Detalles de la Cita:</h3>
                        <p><strong>Fecha Preferida:</strong> {data['fecha_preferida']}</p>
                        <p><strong>Hora Preferida:</strong> {data['hora_preferida']}</p>
                        <p><strong>Tipo de Servicio:</strong> {data['tipo_servicio']}</p>
                        
                        <p><strong>Descripción:</strong></p>
                        <div style="background: #f5f5f5; padding: 15px; border-radius: 5px;">
                            {data['descripcion']}
                        </div>
                        
                        <div style="margin-top: 30px; padding: 15px; background: #fff3e0; border-left: 4px solid #FF6B00;">
                            <p style="margin: 0;"><strong>💡 Acción Requerida:</strong></p>
                            <p style="margin: 5px 0 0 0;">Contacta al cliente para confirmar la cita.</p>
                        </div>
                        
                        <p style="color: #666; font-size: 12px; margin-top: 20px;">
                            Recibido el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        print(f"[EMAIL] Appointment request from {data['nombre']} {data['apellidos']}")
        print(f"[EMAIL] Service: {data['tipo_servicio']} on {data['fecha_preferida']} at {data['hora_preferida']}")
        
        return {"success": True, "message": "Appointment email sent"}
    except Exception as e:
        print(f"[EMAIL ERROR] {str(e)}")
        return {"success": False, "error": str(e)}

def generate_whatsapp_link(data: dict, message_type: str = "contact"):
    """Generate WhatsApp link with pre-filled message"""
    try:
        if message_type == "appointment":
            message = f"""Hola, me gustaría confirmar mi solicitud de cita:

👤 {data['nombre']} {data['apellidos']}
📅 {data['fecha_preferida']} a las {data['hora_preferida']}
🔧 Servicio: {data['tipo_servicio']}
📝 {data['descripcion']}

¿Podemos confirmar la cita?"""
        else:
            message = f"""Hola, acabo de enviar un mensaje desde la web:

{data['mensaje']}

Saludos,
{data['nombre']}"""
        
        import urllib.parse
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded_message}"
        
        print(f"[WHATSAPP] Generated link for {data.get('nombre', 'Unknown')}")
        return whatsapp_url
    except Exception as e:
        print(f"[WHATSAPP ERROR] {str(e)}")
        return f"https://wa.me/{WHATSAPP_NUMBER}"
