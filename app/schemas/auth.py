from pydantic import BaseModel

from app.schemas.user import UserRead


class AuthResponse(BaseModel):
    user: UserRead
    access_token: str