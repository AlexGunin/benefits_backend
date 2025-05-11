from typing import List

from app.schemas.base import  BaseModel, ORMBaseModel

class OrderBase(BaseModel):
    user_id: int
    benefit_ids: List[int]

class OrderCreate(OrderBase):
    pass

class OrderRead(ORMBaseModel):
    id: int
