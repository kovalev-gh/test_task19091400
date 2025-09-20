from fastapi import APIRouter
from core.config import settings

from api.api_v1 import (
    auth,
    applications,
    links,
    users,
    balances,
    rates,
    stats,
)

# общий роутер для /v1
router = APIRouter(prefix=settings.api.v1.prefix)

# подключаем каждый модуль с префиксом из конфига
router.include_router(
    auth.router,
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

router.include_router(
    applications.router,
    prefix=settings.api.v1.applications,
    tags=["Applications"],
)

router.include_router(
    links.router,
    prefix=settings.api.v1.links,
    tags=["Links"],
)

router.include_router(
    users.router,
    prefix=settings.api.v1.users,
    tags=["Users"],
)

router.include_router(
    balances.router,
    prefix=settings.api.v1.balances,
    tags=["Balances"],
)

router.include_router(
    rates.router,
    prefix=settings.api.v1.rates,
    tags=["Rates"],
)

router.include_router(
    stats.router,
    prefix=settings.api.v1.stats,
    tags=["Stats"],
)
