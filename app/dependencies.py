from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request, HTTPException

from app.constants.user import RoleEnum
from app.db.engine import get_session
from app.services.benefits import BenefitsService, get_benefits_service
from app.services.orders import OrdersService, get_orders_service
from app.services.users import UsersService, get_users_service
from app.services.auth import AuthService, get_auth_service


class Services:
    def __init__(self):
        self.benefits = Annotated[BenefitsService, Depends(get_benefits_service)]
        self.orders = Annotated[OrdersService, Depends(get_orders_service)]
        self.users = Annotated[UsersService, Depends(get_users_service)]
        self.users = Annotated[UsersService, Depends(get_users_service)]
        self.auth = Annotated[AuthService, Depends(get_auth_service)]


def get_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")

    return auth_header.split(" ")[1]

# def get_token(request: Request) -> str:
#     token = request.cookies.get("access_token", None)
#     if not token:
#         raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
#     return token


def get_current_user_id(token: str = Depends(get_token), auth_service = Depends(get_auth_service)) -> int:
    data = auth_service.encode_token(token)
    return data["user_id"]

def get_current_user_role(token: str = Depends(get_token), auth_service = Depends(get_auth_service)) -> int:
    data = auth_service.encode_token(token)
    return data["role"]

def is_admin(role = Depends(get_current_user_role)):
    if not role == "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return True


class Dependencies:
    def __init__(self):
        self.session = Annotated[AsyncSession, Depends(get_session)]
        self.services = Services()
        self.user_id = Annotated[int, Depends(get_current_user_id)]
        self.user_role = Annotated[RoleEnum, Depends(get_current_user_role)]
        self.is_admin = Annotated[RoleEnum, Depends(get_current_user_role)]

deps = Dependencies()