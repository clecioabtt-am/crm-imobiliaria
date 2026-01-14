from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.deps import get_current_user
from app.models.contact import Contact
from app.models.property import Property
from app.models.deal import Deal
from app.models.task import Task
from app.models.message import Message
from app.schemas import (
    ContactIn, ContactOut,
    PropertyIn, PropertyOut,
    DealIn, DealOut,
    TaskIn, TaskOut,
    MessageOut
)

router = APIRouter(prefix="/api", tags=["crm"])

# Contacts
@router.get("/contacts", response_model=list[ContactOut])
def list_contacts(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Contact).order_by(Contact.id.desc()).all()

@router.post("/contacts", response_model=ContactOut)
def create_contact(payload: ContactIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    c = Contact(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.put("/contacts/{contact_id}", response_model=ContactOut)
def update_contact(contact_id: int, payload: ContactIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    c = db.query(Contact).filter(Contact.id == contact_id).first()
    if not c:
        raise HTTPException(404, "Contato não encontrado")
    for k,v in payload.model_dump().items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c

# Properties
@router.get("/properties", response_model=list[PropertyOut])
def list_properties(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Property).order_by(Property.id.desc()).all()

@router.post("/properties", response_model=PropertyOut)
def create_property(payload: PropertyIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = Property(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.put("/properties/{property_id}", response_model=PropertyOut)
def update_property(property_id: int, payload: PropertyIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = db.query(Property).filter(Property.id == property_id).first()
    if not p:
        raise HTTPException(404, "Imóvel não encontrado")
    for k,v in payload.model_dump().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

# Deals
@router.get("/deals", response_model=list[DealOut])
def list_deals(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Deal).order_by(Deal.id.desc()).all()

@router.post("/deals", response_model=DealOut)
def create_deal(payload: DealIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    d = Deal(**payload.model_dump())
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

@router.put("/deals/{deal_id}", response_model=DealOut)
def update_deal(deal_id: int, payload: DealIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    d = db.query(Deal).filter(Deal.id == deal_id).first()
    if not d:
        raise HTTPException(404, "Negócio não encontrado")
    for k,v in payload.model_dump().items():
        setattr(d, k, v)
    db.commit()
    db.refresh(d)
    return d

# Tasks
@router.get("/tasks", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Task).order_by(Task.id.desc()).all()

@router.post("/tasks", response_model=TaskOut)
def create_task(payload: TaskIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    t = Task(**payload.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t:
        raise HTTPException(404, "Tarefa não encontrada")
    for k,v in payload.model_dump().items():
        setattr(t, k, v)
    db.commit()
    db.refresh(t)
    return t

# Messages per contact (timeline)
@router.get("/contacts/{contact_id}/messages", response_model=list[MessageOut])
def list_messages(contact_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Message).filter(Message.contact_id == contact_id).order_by(Message.id.asc()).all()
