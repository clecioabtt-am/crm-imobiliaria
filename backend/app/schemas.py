from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "broker"

class ContactIn(BaseModel):
    name: Optional[str] = None
    phone: str
    stage: Optional[str] = "Novo lead"
    source: Optional[str] = "WhatsApp"
    notes: Optional[str] = ""

class ContactOut(ContactIn):
    id: int
    created_at: datetime

class PropertyIn(BaseModel):
    title: str
    type: str = "Apartamento"
    neighborhood: str = ""
    city: str = ""
    price: float = 0
    purpose: str = "Venda"
    status: str = "Disponível"
    description: str = ""

class PropertyOut(PropertyIn):
    id: int
    created_at: datetime

class DealIn(BaseModel):
    contact_id: int
    property_id: Optional[int] = None
    stage: str = "Qualificando"
    value: float = 0
    assigned_to_user_id: Optional[int] = None

class DealOut(DealIn):
    id: int
    created_at: datetime

class TaskIn(BaseModel):
    title: str
    deal_id: Optional[int] = None
    contact_id: Optional[int] = None
    assigned_to_user_id: Optional[int] = None
    status: str = "Aberta"
    due_at: Optional[datetime] = None

class TaskOut(TaskIn):
    id: int
    created_at: datetime

class MessageOut(BaseModel):
    id: int
    contact_id: int
    direction: str
    content: str
    wa_message_id: str
    created_at: datetime
