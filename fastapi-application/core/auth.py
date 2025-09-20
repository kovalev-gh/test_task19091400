import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from core.config import settings


SECRET_KEY = settings.jwt.secret
ALGORITHM = settings.jwt.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt.expire_minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля с хешем"""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Хеширование пароля"""
    return pwd_context.hash(password)


def create_jwt(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    """Создание JWT с временем жизни"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str) -> dict:
    """Декодирование и проверка JWT"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")


async def get_current_user(credentials=Depends(security)) -> dict:
    """
    Достаёт токен из заголовка Authorization: Bearer <token>
    и возвращает декодированные claims.
    """
    token = credentials.credentials
    return decode_jwt(token)
