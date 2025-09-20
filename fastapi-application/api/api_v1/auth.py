from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import User
from core.models.db_helper import db_helper
from core.schemas.auth import LoginIn, TokenRead
from core.schemas.user import UserRead
from core.auth import create_jwt, get_current_user, verify_password, hash_password

#router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])
router = APIRouter()

@router.post("/login", response_model=TokenRead)
async def login(
    data: LoginIn,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Реальный логин:
    - ищем пользователя по email (username = часть до @).
    - сверяем введённый пароль с хешем в БД.
    - при успехе выдаём JWT.
    """
    username = data.email.split("@")[0]

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Invalid email or password")

    token = create_jwt({"user_id": user.id, "email": data.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead)
async def register(
    data: LoginIn,  # используем LoginIn (email + password)
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Регистрация нового пользователя:
    - username = часть email до "@"
    - пароль хешируется и сохраняется
    """
    username = data.email.split("@")[0]

    result = await db.execute(select(User).where(User.username == username))
    if result.scalar_one_or_none():
        raise HTTPException(400, "User already exists")

    user = User(
        username=username,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/me", response_model=UserRead)
async def me(
    claims=Depends(get_current_user),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Возвращает профиль текущего пользователя.
    """
    result = await db.execute(select(User).where(User.id == claims["user_id"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return user
