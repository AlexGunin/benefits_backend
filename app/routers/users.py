from typing import List

from fastapi import APIRouter

from app.dependencies import deps
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("", response_model=UserRead)
async def create_user(user: UserCreate, users_service: deps.services.users):
    return await users_service.add(user)

@router.get("", response_model=List[UserRead])
async def get_users(users_service: deps.services.users):
    return await users_service.get_all()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, users_service: deps.services.users):
    return await users_service.get_one(user_id)

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_data: UserUpdate, users_service: deps.services.users):
    return await users_service.patch(user_id, user_data)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, users_service: deps.services.users):
    return await users_service.delete(user_id)