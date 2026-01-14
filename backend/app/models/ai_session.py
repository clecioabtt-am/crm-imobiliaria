from sqlalchemy import String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database import Base

class AISession(Base):
    __tablename__ = "ai_sessions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contact_id: Mapped[int] = mapped_column(Integer, ForeignKey("contacts.id"), unique=True, nullable=False)
    last_intent: Mapped[str] = mapped_column(String(120), default="")
    context_json: Mapped[str] = mapped_column(String(8000), default="{}")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
