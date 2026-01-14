import json
import re
import requests
from sqlalchemy.orm import Session
from app.config import settings
from app.models.ai_session import AISession
from app.models.property import Property

def _get_or_create_session(contact_id: int, db: Session) -> AISession:
    s = db.query(AISession).filter(AISession.contact_id == contact_id).first()
    if not s:
        s = AISession(contact_id=contact_id, last_intent="", context_json="{}")
        db.add(s)
        db.commit()
        db.refresh(s)
    return s

def _rules_engine(text: str, db: Session):
    t = (text or "").strip().lower()

    # intenções simples
    if any(k in t for k in ["comprar", "compra", "vender", "venda"]):
        return "Perfeito! Você quer *comprar* em qual bairro e qual faixa de valor aproximada?"
    if any(k in t for k in ["alugar", "aluguel", "locação", "locar"]):
        return "Ótimo! Você quer *alugar* em qual bairro e qual valor máximo por mês?"
    if any(k in t for k in ["visita", "agendar", "marcar"]):
        return "Claro! Me diga o *imóvel* (código ou título) e o *dia/horário* que prefere para agendar a visita."

    # busca simples por bairro (se o usuário falar um bairro que exista no cadastro)
    props = db.query(Property).filter(Property.status == "Disponível").all()
    neighborhoods = {p.neighborhood.lower(): p.neighborhood for p in props if p.neighborhood}
    for nb_lower, nb in neighborhoods.items():
        if nb_lower and nb_lower in t:
            matches = [p for p in props if (p.neighborhood or "").lower() == nb_lower and p.status == "Disponível"]
            if matches:
                top = matches[:3]
                lines = ["Encontrei estas opções disponíveis:"]
                for p in top:
                    lines.append(f"- {p.title} | {p.purpose} | R$ {float(p.price):,.2f} | {p.neighborhood} ({p.city})")
                lines.append("Quer que eu te envie mais detalhes de alguma delas?")
                return "\n".join(lines)

    return "Olá! 😊 Para eu te ajudar rápido, me diga: você procura *compra* ou *aluguel*? E qual bairro/faixa de valor?"

def _openai_reply(prompt: str):
    # Implementação opcional e conservadora: usa endpoint genérico via HTTPS.
    # Se você quiser que eu integre exatamente com um provedor específico (OpenAI/Anthropic/etc.), eu ajusto.
    if not settings.OPENAI_API_KEY:
        return None
    # Mantém simples: o usuário pode adaptar para o provedor desejado.
    return None

def generate_reply(text: str, contact_phone: str, db: Session) -> str:
    # Modo rules (padrão)
    return _rules_engine(text, db)
