from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.schemas.applications import ApplicationCreate, ApplicationRead
from core.auth import get_current_user
from core.models.db_helper import db_helper
from core.models import Application
from crud import applications as crud_app
from crud.links import assign_trader

router = APIRouter()


@router.post("", response_model=ApplicationRead)
async def create_application(
    data: ApplicationCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
    user: dict = Depends(get_current_user),
):
    """Создать заявку"""
    return await crud_app.create_application(db, user["user_id"], data)


@router.get("", response_model=list[ApplicationRead])
async def list_applications(
    db: AsyncSession = Depends(db_helper.session_getter),
    user: dict = Depends(get_current_user),
):
    """Список заявок текущего пользователя"""
    return await crud_app.list_applications(db, user["user_id"])


@router.post("/{app_id}/confirm", response_model=ApplicationRead)
async def confirm_application(
    app_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
    user: dict = Depends(get_current_user),
):
    """Подтвердить заявку (спишется комиссия 1.5%)"""
    return await crud_app.confirm_application(db, user["user_id"], app_id)


@router.post("/{app_id}/cancel", response_model=ApplicationRead)
async def cancel_application(
    app_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
    user: dict = Depends(get_current_user),
):
    """Отменить заявку (если не approved)"""
    return await crud_app.cancel_application(db, user["user_id"], app_id)


@router.post("/{app_id}/assign-trader", response_model=ApplicationRead)
async def reassign_trader(
    app_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
    user: dict = Depends(get_current_user),
):
    """Повторно назначить трейдера для заявки"""
    res = await db.execute(
        select(Application).where(
            Application.id == app_id,
            Application.user_id == user["user_id"],
        )
    )
    app = res.scalar_one_or_none()
    if not app:
        raise HTTPException(404, "Application not found")

    trader_id = await assign_trader(db, app.merchant_id, app)
    if trader_id is None:
        raise HTTPException(400, "No suitable trader found")

    app.trader_id = trader_id
    await db.commit()
    await db.refresh(app)
    return app
