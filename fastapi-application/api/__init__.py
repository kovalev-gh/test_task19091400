from fastapi import APIRouter
from core.config import settings
from api import v1

# общий роутер для /api
router = APIRouter(prefix=settings.api.prefix)

# вешаем v1 на общий /api
router.include_router(v1.router)
