from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.user import UserModel
from app.repositories.base.sql_alchemy import SQLAlchemyRepository
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.exceptions import DatabaseError

class UsersRepository(SQLAlchemyRepository[UserModel, UserCreate, UserUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)

    async def add_one(self, data: UserCreate) -> UserRead:
        try:
            obj = self.model(**data)
            self.session.add(obj)
            await self.session.flush()
            await self.session.refresh(obj)

            return UserRead.model_validate(obj)

        except Exception as e:
            raise DatabaseError(f"Ошибка при добавлении объекта: {str(e)}")

    async def get_by_nick(self, nick: str) -> UserModel:
        query = select(self.model).filter_by(nickname=nick)
        try:
            entity = await self.session.execute(query)
        except Exception as e:
            raise DatabaseError(str(e))

        return entity.scalars().one_or_none()
