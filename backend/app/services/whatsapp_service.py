import requests
from sqlalchemy.orm import Session
from app.config import settings
from app.models.contact import Contact
from app.models.message import Message
from app.services.ai_agent import generate_reply

def _send_whatsapp_text(to_phone: str, text: str):
    if not settings.WHATSAPP_TOKEN or not settings.WHATSAPP_PHONE_NUMBER_ID:
        # Sem credenciais configuradas: não envia, mas mantém o sistema funcional
        return None

    url = f"https://graph.facebook.com/{settings.WHATSAPP_API_VERSION}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "text",
        "text": {"body": text},
    }
    r = requests.post(url, headers=headers, json=payload, timeout=20)
    try:
        return r.json()
    except Exception:
        return {"status_code": r.status_code, "text": r.text}

def process_incoming_webhook(data: dict, db: Session):
    # Estrutura padrão do webhook: entry -> changes -> value -> messages
    entry = (data.get("entry") or [])
    for e in entry:
        for change in (e.get("changes") or []):
            value = change.get("value") or {}
            messages = value.get("messages") or []
            for msg in messages:
                from_phone = msg.get("from")  # número do cliente
                text_body = (msg.get("text") or {}).get("body", "")
                wa_id = msg.get("id", "")

                if not from_phone or not text_body:
                    continue

                contact = db.query(Contact).filter(Contact.phone == from_phone).first()
                if not contact:
                    contact = Contact(phone=from_phone, name=None, stage="Novo lead", source="WhatsApp")
                    db.add(contact)
                    db.commit()
                    db.refresh(contact)

                db.add(Message(contact_id=contact.id, direction="in", content=text_body, wa_message_id=wa_id))
                db.commit()

                # IA responde (ou regras)
                reply = generate_reply(text_body, contact_phone=from_phone, db=db)

                # Envia resposta no WhatsApp
                send_resp = _send_whatsapp_text(from_phone, reply)

                # Salva no CRM como mensagem de saída
                db.add(Message(contact_id=contact.id, direction="out", content=reply, wa_message_id=str((send_resp or {}).get("messages", [{}])[0].get("id",""))))
                db.commit()
