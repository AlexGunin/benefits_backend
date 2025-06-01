from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from io import BytesIO
import pandas as pd

from app.db.engine import get_session
from app.db.models.order import OrderModel
from app.repositories.orders import OrdersRepository
from app.schemas.order import OrderCreate, OrderRead
from app.services.base import BaseService


class OrdersService(BaseService[OrderModel, OrderCreate, None]):
    def __init__(self, orders_repository: OrdersRepository):
        super().__init__(repository=orders_repository)

    async def get_excel(self, has_empty: bool | None):
        result = await self.repository.session.execute(select(self.repository.model))

        rows = [OrderRead.model_validate(order).model_dump() for order in result.scalars().all()]

        flat_rows = []

        for row in rows:
            order_id = row["id"]
            user_id = row["user_id"]
            snapshot = row.get("snapshot", [])

            if snapshot:
                for item in snapshot:
                    flat_rows.append({
                        "order_id": order_id,
                        "user_id": user_id,
                        "benefit_id": item["id"],
                        "benefit_name": item["name"],
                        "scope": item["scope"],
                        "price": item["price"],
                        "quantity": item["quantity"],
                        "created_at": row["created_at"]
                    })
            elif has_empty:
                flat_rows.append({
                    "order_id": order_id,
                    "user_id": user_id,
                    "scope": None,
                    "benefit_id": None,
                    "benefit_name": None,
                    "price": None,
                    "quantity": None,
                    "created_at": None
                })

        df = pd.DataFrame(flat_rows)

        stream = BytesIO()
        with pd.ExcelWriter(stream, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Users")
        stream.seek(0)

        return stream

def get_orders_service(session: AsyncSession = Depends(get_session)):
    return OrdersService(OrdersRepository(session))