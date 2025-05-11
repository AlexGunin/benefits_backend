from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.db.engine import get_session
from app.db.models.order import OrderModel
from app.repositories.base.abstract import AbstractRepository
from app.repositories.orders import OrdersRepository
from app.schemas.order import OrderCreate
from app.services.base import BaseService


class OrdersService(BaseService[OrderModel, OrderCreate, None]):
    def __init__(self, orders_repository: AbstractRepository[OrderModel, OrderCreate, None]):
        super().__init__(repository=orders_repository)


def get_orders_service(session: AsyncSession = Depends(get_session)):
    return OrdersService(OrdersRepository(session))