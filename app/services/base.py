from app.repositories.base.abstract import AbstractRepository

from abc import ABC
from typing import TypeVar, Generic

Model = TypeVar('Model')
CreateSchema = TypeVar('CreateSchema')
UpdateSchema = TypeVar('UpdateSchema')

class BaseService(ABC, Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(self, repository: AbstractRepository[Model, CreateSchema, UpdateSchema]):
        self.repository: AbstractRepository[Model, CreateSchema, UpdateSchema] = repository

    async def add(self, data: CreateSchema) -> int:
        return await self.repository.add_one(data.model_dump())

    async def get_all(self):
        return await self.repository.list_all()

    async def get_one(self, id: int):
        return await self.repository.get_by_id(id)

    async def patch(self, id: int, data: UpdateSchema):
        return await self.repository.update_one(id, data)

    async def delete(self, id: int):
        return await self.repository.delete_one(id)