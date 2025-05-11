from fastapi import APIRouter
from app.routers import benefits, users, orders, auth


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(benefits.router)
api_router.include_router(users.router)
api_router.include_router(orders.router)
