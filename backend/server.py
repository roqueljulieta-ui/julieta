from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from models import ContactForm, ContactFormCreate, AppointmentForm, AppointmentFormCreate
from email_service import send_contact_email, send_appointment_email, generate_whatsapp_link
from typing import List


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI()

# Create API router
api_router = APIRouter(prefix="/api")


# Health check
@api_router.get("/")
async def root():
    return {"message": "Services Truck API - Running", "status": "ok"}


# Contact Form Endpoints
@api_router.post("/contact", response_model=ContactForm)
async def submit_contact_form(form_data: ContactFormCreate):
    """Submit contact form and send email notification"""
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
    """Get all contact forms"""
    try:
        forms = await db.contact_forms.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
        for form in forms:
            if isinstance(form.get('created_at'), str):
                from datetime import datetime
                form['created_at'] = datetime.fromisoformat(form['created_at'])
        return forms
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Appointment Endpoints
@api_router.post("/appointments", response_model=AppointmentForm)
async def create_appointment(appointment_data: AppointmentFormCreate):
    """Create appointment and send notifications"""
    try:
        appointment = AppointmentForm(**appointment_data.model_dump())
        doc = appointment.model_dump()
        doc['created_at'] = doc['created_at'].isoformat()
        await db.appointments.insert_one(doc)
        send_appointment_email(appointment_data.model_dump())
        logging.info(f"Appointment: {appointment.nombre} {appointment.apellidos}")
        return appointment
    except Exception as e:
        logging.error(f"Appointment error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@api_router.get("/appointments", response_model=List[AppointmentForm])
async def get_appointments():
    """Get all appointments"""
    try:
        appointments = await db.appointments.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
        for apt in appointments:
            if isinstance(apt.get('created_at'), str):
                from datetime import datetime
                apt['created_at'] = datetime.fromisoformat(apt['created_at'])
        return appointments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WhatsApp link generator
@api_router.post("/whatsapp/generate")
async def generate_whatsapp_message(data: dict):
    """Generate WhatsApp link"""
    try:
        message_type = data.get("type", "contact")
        link = generate_whatsapp_link(data, message_type)
        return {"whatsapp_link": link}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Include router
app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
