import asyncio
from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from models import ContactForm, ContactFormCreate, AppointmentForm, AppointmentFormCreate
from email_service import (
    send_contact_email,
    send_appointment_email,
    send_appointment_received_email,
    send_appointment_confirmed_email,
    generate_whatsapp_link,
)
from typing import List


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    return {"message": "Services Truck API - Running", "status": "ok"}


@api_router.post("/contact", response_model=ContactForm)
async def submit_contact_form(form_data: ContactFormCreate):
    try:
        contact = ContactForm(**form_data.model_dump())
        doc = contact.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.contact_forms.insert_one(doc)
        send_contact_email(form_data.model_dump())
        return contact
    except Exception as e:
        logging.error(f"Contact form error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@api_router.get("/contact", response_model=List[ContactForm])
async def get_contact_forms():
    try:
        forms = await db.contact_forms.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
        for form in forms:
            if isinstance(form.get('created_at'), str):
                from datetime import datetime
                form['created_at'] = datetime.fromisoformat(form['created_at'])
        return forms
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _delayed_received_email(data: dict):
    await asyncio.sleep(180)
    send_appointment_received_email(data)


@api_router.post("/appointments", response_model=AppointmentForm)
async def create_appointment(appointment_data: AppointmentFormCreate, background_tasks: BackgroundTasks):
    try:
        appointment = AppointmentForm(**appointment_data.model_dump())
        doc = appointment.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        doc['status'] = 'pending'
        await db.appointments.insert_one(doc)

        send_appointment_email(appointment_data.model_dump(), appointment.id)
        background_tasks.add_task(_delayed_received_email, appointment_data.model_dump())

        logging.info(f"Appointment: {appointment.nombre} {appointment.apellidos}")
        return appointment
    except Exception as e:
        logging.error(f"Appointment error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@api_router.get("/appointments", response_model=List[AppointmentForm])
async def get_appointments():
    try:
        appointments = await db.appointments.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
        for apt in appointments:
            if isinstance(apt.get('created_at'), str):
                from datetime import datetime
                apt['created_at'] = datetime.fromisoformat(apt['created_at'])
        return appointments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/appointments/{appointment_id}/confirm", response_class=HTMLResponse)
async def confirm_appointment(appointment_id: str):
    try:
        appointment = await db.appointments.find_one({"id": appointment_id})
        if not appointment:
            return HTMLResponse("<h2>Cita no encontrada.</h2>", status_code=404)

        if appointment.get("status") == "confirmed":
            return HTMLResponse(
                "<html><body style='font-family: Arial, sans-serif; text-align:center; padding: 60px;'>"
                "<h2>Esta cita ya habia sido confirmada anteriormente.</h2>"
                "</body></html>"
            )

        await db.appointments.update_one({"id": appointment_id}, {"$set": {"status": "confirmed"}})
        send_appointment_confirmed_email(appointment)

        return HTMLResponse(
            "<html><body style='font-family: Arial, sans-serif; text-align:center; padding: 60px;'>"
            "<h2 style='color:#0A1929;'>Cita confirmada correctamente</h2>"
            "<p>Se ha enviado un correo de confirmacion al cliente. Ya puedes cerrar esta pestana.</p>"
            "</body></html>"
        )
    except Exception as e:
        return HTMLResponse("<h2>Error: " + str(e) + "</h2>", status_code=500)


@api_router.post("/whatsapp/generate")
async def generate_whatsapp_message(data: dict):
    try:
        message_type = data.get("type", "contact")
        link = generate_whatsapp_link(data, message_type)
        return {"whatsapp_link": link}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
