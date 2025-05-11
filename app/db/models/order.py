from typing import TypedDict

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON

from app.db.models.base import Base

class BenefitSnapshot(TypedDict):
    id: int
    name: str
    description: str | None
    price: int
    scope: str
    quantity: int

class OrderModel(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="orders")

    snapshot: Mapped[list[BenefitSnapshot]] = mapped_column(JSON)  # 👈 Тут конкретный тип!