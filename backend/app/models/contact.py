from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=True)
    phone: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)  # E.164 recomendado
    stage: Mapped[str] = mapped_column(String(60), default="Novo lead")
    source: Mapped[str] = mapped_column(String(60), default="WhatsApp")
    notes: Mapped[str] = mapped_column(String(2000), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
