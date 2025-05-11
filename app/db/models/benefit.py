from sqlalchemy.orm import Mapped, mapped_column

from app.constants.benefit import ScopeEnum
from app.db.models.base import Base

class BenefitModel(Base):
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    max_usage: Mapped[int | None]
    scope: Mapped[ScopeEnum] = mapped_column(default=ScopeEnum.SELF)