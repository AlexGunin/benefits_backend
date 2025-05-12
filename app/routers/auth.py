from fastapi import APIRouter, HTTPException, Response

from app.constants.user import RoleEnum
from app.dependencies import deps
from app.schemas.auth import AuthResponse
from app.schemas.user import UserCreate, UserLogin, UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=AuthResponse)
async def register_user(
        data: UserCreate,
        auth_service: deps.services.auth,
        session: deps.session,
        user_service: deps.services.users,
):
    try:
        user = await user_service.get_by_nick(data.nickname)

        if user:
            raise HTTPException(status_code=409, detail="Пользователь с таким nickname уже существует")

        hashed_password = auth_service.hash_password(data.password)
        new_user_data = UserCreate(name=data.name, nickname=data.nickname, password=hashed_password, role=data.role)
        created_user = await user_service.add(new_user_data)

        access_token = auth_service.create_access_token({"user_id": user.id, "role": user.role})
        # response.set_cookie("access_token", access_token, samesite="none", httponly=True, secure=True, )

        await session.commit()

        return {"user": UserRead.model_validate(created_user), "access_token": access_token}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка создания пользователя: {str(e)}")



@router.post("/login", response_model=AuthResponse)
async def login_user(
        data: UserLogin,
        user_service: deps.services.users,
        auth_service: deps.services.auth
):
    user = await user_service.get_by_nick(data.nickname)

    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким nickname не зарегистрирован")

    if not auth_service.verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Пароль неверный")

    access_token = auth_service.create_access_token({"user_id": user.id, "role": user.role})
    # response.set_cookie("access_token", access_token, samesite="none", httponly=True,secure=True,)


    return {"user": UserRead.model_validate(user), "access_token":access_token }


@router.post("/anonym", response_model=AuthResponse)
async def login_anonym(
        user_service: deps.services.users,
        auth_service: deps.services.auth,
        session: deps.session,
):
    new_user_data = UserCreate(name="Anonym", nickname="anonym", password="123", role=RoleEnum.USER)

    created_user = await user_service.add(new_user_data)

    await session.commit()

    access_token = auth_service.create_access_token({"user_id": created_user.id, "role": created_user.role})

    return {"user": UserRead.model_validate(created_user), "access_token":access_token }

@router.get("/me", response_model=UserRead)
async def get_me(
        user_id: deps.user_id,
        users_service: deps.services.users
):
    user = await users_service.get_one(user_id)

    return UserRead.model_validate(user)


@router.post("/logout")
async def logout():
    # response.delete_cookie("access_token")
    return {"status": "OK"}
