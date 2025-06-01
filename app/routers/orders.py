from typing import List

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.dependencies import deps
from app.schemas.benefit import BenefitInOrder
from app.schemas.order import OrderCreate, OrderRead

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("", response_model=OrderRead)
async def create_order(user_id: deps.user_id, benefits: List[BenefitInOrder], orders_service: deps.services.orders):
    order = OrderCreate(user_id=user_id, snapshot=benefits)
    return await orders_service.add(order)


@router.get("", response_model=List[OrderRead])
async def get_orders(orders_service: deps.services.orders):
    return await orders_service.get_all()


@router.get("/excel")
async def get_excel_orders(
        orders_service: deps.services.orders,
        has_empty: bool = Query(False, description="Включать пустые заказы?")
):
    stream = await orders_service.get_excel(has_empty)

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=orders.xlsx"}
    )


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: int, orders_service: deps.services.orders):
    return await orders_service.get_one(order_id)


@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int, orders_service: deps.services.orders):
    return await orders_service.delete(order_id)
