from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.deps import get_current_user
from app.services.ai_agent import generate_reply

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/preview")
def preview(payload: dict, db: Session = Depends(get_db), _=Depends(get_current_user)):
    text = payload.get("text","")
    phone = payload.get("phone","")
    return {"reply": generate_reply(text, phone, db)}
