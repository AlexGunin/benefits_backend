from typing import Optional

from app.db.models.user import RoleEnum
from app.schemas.base import BaseModel, ORMBaseModel

class UserBase(BaseModel):
    name: str | None
    nickname: str
    role: RoleEnum | None

    class Config:
        use_enum_values = True
        from_attributes = True

class UserLogin(BaseModel):
    nickname: str
    password: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase, ORMBaseModel):
    id: int

class UserUpdate(ORMBaseModel):
    name: str | None
    nickname: str | None
    password: str | None
    role: RoleEnum | None