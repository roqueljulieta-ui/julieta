from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid

class ContactForm(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str
    email: EmailStr
    telefono: str
    mensaje: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"

class ContactFormCreate(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str
    mensaje: str

class AppointmentForm(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str
    fecha_preferida: str
    hora_preferida: str
    tipo_servicio: str
    descripcion: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"

class AppointmentFormCreate(BaseModel):
    nombre: str
    apellidos: str
    email: EmailStr
    telefono: str
    fecha_preferida: str
    hora_preferida: str
    tipo_servicio: str
    descripcion: str
