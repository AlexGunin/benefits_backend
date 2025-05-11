from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.engine import get_session
from app.db.models.user import UserModel
from app.repositories.users import UsersRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService


class UsersService(BaseService[UserModel, UserCreate, UserUpdate]):
    def __init__(self, users_repository: UsersRepository):
        super().__init__(repository=users_repository)


    async def get_by_nick(self, nick: str):
        return await self.repository.get_by_nick(nick)


def get_users_service(session: AsyncSession = Depends(get_session)):
    return UsersService(UsersRepository(session))