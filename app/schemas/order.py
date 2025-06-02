from typing import List
from datetime import datetime
from app.schemas.base import  BaseModel, ORMBaseModel
from app.schemas.benefit import BenefitInOrder

class OrderBase(BaseModel):
    user_id: int
    snapshot: List[BenefitInOrder]

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase, ORMBaseModel):
    id: int
    created_at: datetime
