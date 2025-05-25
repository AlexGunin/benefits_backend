from fastapi import APIRouter
from app.dependencies import deps

router = APIRouter(
    prefix="/limit",
    tags=["Limit"],
)

@router.get("")
async def get_limit_by_user(user_id: deps.user_id):
    return 80000