from typing import List

from fastapi import APIRouter

from app.dependencies import deps
from app.schemas.order import OrderCreate, OrderRead

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("", response_model=OrderRead)
async def create_order(order: OrderCreate, orders_service: deps.services.orders):
    return await orders_service.add(order)

@router.get("", response_model=List[OrderRead])
async def get_orders(orders_service: deps.services.orders):
    return await orders_service.get_all()


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, orders_service: deps.services.orders):
    return await orders_service.get_one(order_id)

@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int, orders_service: deps.services.orders):
    return await orders_service.delete(order_id)