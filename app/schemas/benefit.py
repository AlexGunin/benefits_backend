from pydantic import BaseModel, Field

from app.constants.benefit import ScopeEnum
from app.schemas.base import ORMBaseModel

class BenefitInOrder(BaseModel):
    id: int
    name: str
    description: str | None
    price: int
    scope: str
    quantity: int

class BenefitBase(BaseModel):
    name: str
    description: str | None
    price: int = Field(ge=0)
    max_usage: int | None = Field(None, ge=0)
    scope: ScopeEnum

class BenefitCreate(BenefitBase):
    pass

class BenefitRead(BenefitBase, ORMBaseModel):
    id: int

class BenefitUpdate(ORMBaseModel):
    name: str | None
    scope: ScopeEnum | None
    description: str | None
    price: int | None
    category_id: int | None
