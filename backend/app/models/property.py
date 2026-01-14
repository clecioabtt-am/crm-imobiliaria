from sqlalchemy import String, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database import Base

class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(60), default="Apartamento")
    neighborhood: Mapped[str] = mapped_column(String(120), default="")
    city: Mapped[str] = mapped_column(String(120), default="")
    price: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    purpose: Mapped[str] = mapped_column(String(30), default="Venda")  # Venda|Aluguel
    status: Mapped[str] = mapped_column(String(30), default="Disponível")  # Disponível|Reservado|Vendido|Alugado
    description: Mapped[str] = mapped_column(String(4000), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
