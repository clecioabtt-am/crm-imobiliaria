from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.services.whatsapp_service import process_incoming_webhook

router = APIRouter(prefix="/webhook/whatsapp", tags=["whatsapp"])

# Verificação do webhook (Meta)
@router.get("")
def verify(hub_mode: str = "", hub_challenge: str = "", hub_verify_token: str = ""):
    # A Meta envia query params: hub.mode, hub.challenge, hub.verify_token
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(403, "Falha na verificação do webhook")

@router.post("")
async def webhook(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    process_incoming_webhook(data, db)
    return {"status": "ok"}
