from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Type, TypeVar, List, Generic

from app.exceptions import DatabaseError, NotFoundError
from app.repositories.base.abstract import AbstractRepository

Model = TypeVar('Model')
CreateSchema = TypeVar('CreateSchema')
UpdateSchema = TypeVar('UpdateSchema')

class SQLAlchemyRepository(AbstractRepository[Model, CreateSchema, UpdateSchema], Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, session: AsyncSession, model: Type[Model]):
        self.session: AsyncSession = session
        self.model: Type[Model] = model

    async def add_one(self, data: CreateSchema) -> Model:
        try:
            obj = self.model(**data)
            self.session.add(obj)
            await self.session.flush()
            await self.session.refresh(obj)
            await self.session.commit()
            return obj

        except Exception as e:
            raise DatabaseError(f"Ошибка при добавлении объекта: {str(e)}")

    async def get_by_id(self, id: int) -> Model:
        try:
            entity = await self.session.get(self.model, id)
        except Exception as e:
            raise DatabaseError(str(e))

        if not entity:
            raise NotFoundError(self.model.__name__, id)

        return entity

    async def update_one(self, id: int, data: UpdateSchema):
        try:
            entity = await self.get_by_id(id)

            for key, value in data.dict(exclude_unset=True).items():
                setattr(entity, key, value)

            await self.session.commit()
            await self.session.refresh(entity)

        except NotFoundError as e:
            raise e
        except Exception as e:
            raise DatabaseError(str(e))


    async def list_all(self) -> List[Model]:
        try:
            result = await self.session.execute(select(self.model))

            return result.scalars().all()
        except Exception as e:
            raise DatabaseError(str(e))


    async def delete_one(self, id: int) -> int:
        try:
            entity = await self.get_by_id(id)

            await self.session.delete(entity)
            await self.session.commit()

            return id
        except NotFoundError as e:
            raise e
        except Exception as e:
            raise DatabaseError(str(e))