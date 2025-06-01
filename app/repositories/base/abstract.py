from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

from sqlalchemy.ext.asyncio import AsyncSession

Model = TypeVar('Model')
CreateSchema = TypeVar('CreateSchema')
UpdateSchema = TypeVar('UpdateSchema')

class AbstractRepository(ABC, Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, session: AsyncSession, model: Model):
        self.session: AsyncSession = session
        self.model: Model = model

    @abstractmethod
    async def add_one(self, data: CreateSchema) -> Model:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Model | None:
        pass

    @abstractmethod
    async def list_all(self) -> List[Model]:
        pass

    @abstractmethod
    async def update_one(self, id: int, data: UpdateSchema) -> Model:
        pass

    @abstractmethod
    async def delete_one(self, id: int) -> None:
        pass



