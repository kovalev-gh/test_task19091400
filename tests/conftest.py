import sys
import os
import asyncio
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

# --- Подкладываем минимальные ENV до импорта core.config ---
os.environ.setdefault("APP_CONFIG__DB__URL", "postgresql+asyncpg://user:pass@localhost/db")
os.environ.setdefault("APP_CONFIG__JWT__SECRET", "testsecret")
os.environ.setdefault("APP_CONFIG__JWT__ALGORITHM", "HS256")
os.environ.setdefault("APP_CONFIG__JWT__EXPIRE_MINUTES", "60")

# фиксируем sys.path, чтобы видеть fastapi-application
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "fastapi-application"))

from create_fastapi_app import create_app
from api import router as api_router
from core.models.base import Base
from core.models import db_helper
from core.models.user import User
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# --- создаём свой SQLite engine ---
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(TEST_DB_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Отдельный event loop для асинхронных тестов"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    """Создаём таблицы и тестового пользователя в SQLite"""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # создаём тестового пользователя (id=1)
    async with AsyncSessionLocal() as session:
        user = User(id=1, username="testuser", hashed_password="fake")
        session.add(user)
        await session.commit()

    yield

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture()
async def client():
    app = create_app()
    app.include_router(api_router)

    # мок get_current_user
    async def override_get_current_user():
        return {"user_id": 1, "email": "test@example.com"}

    from core.auth import get_current_user
    app.dependency_overrides[get_current_user] = override_get_current_user

    # ✅ мок db_helper: исключаем local_kw
    async def override_session_getter():
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[db_helper.session_getter] = override_session_getter

    # лог роутов
    print("\n=== Registered routes in TEST APP ===")
    for r in app.routes:
        methods = ",".join(r.methods or [])
        print(f"{methods:10} {r.path}")
    print("=====================================\n")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
