from app.db.models.order import OrderModel
from app.repositories.base.sql_alchemy import SQLAlchemyRepository

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.order import OrderCreate


class OrdersRepository(SQLAlchemyRepository[OrderModel, OrderCreate, None]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrderModel)