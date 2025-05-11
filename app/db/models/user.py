from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants.user import RoleEnum
from app.db.models.base import Base

class UserModel(Base):
    name: Mapped[str]
    nickname: Mapped[str]
    password: Mapped[str]
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.USER)
    orders: Mapped[list["Order"]] = relationship(
        "OrderModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )