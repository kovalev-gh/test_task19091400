from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import List

from core.models import Application, ApplicationStatus, User, BalanceTransaction
from core.schemas.applications import ApplicationCreate

Q6 = Decimal("0.000001")
COMMISSION_PCT = Decimal("1.5")

# мок-курсы (как в /rates)
RATES = {
    "USDT": Decimal("1"),
    "USD": Decimal("1"),
    "INR": Decimal("84"),
    "RUB": Decimal("90"),
}


def to_usdt(amount: Decimal, currency: str) -> Decimal:
    rate = RATES.get(currency.upper())
    if not rate:
        raise HTTPException(400, f"Unsupported currency {currency}")
    return (amount / rate).quantize(Q6, rounding=ROUND_HALF_UP)


async def create_application(
    db: AsyncSession,
    user_id: int,
    data: ApplicationCreate,
) -> Application:
    """Создание заявки: конвертация в USDT, статус = created"""
    amount_original = Decimal(str(data.amount_original))
    amount_usdt = to_usdt(amount_original, data.currency)

    app = Application(
        user_id=user_id,
        merchant_id=user_id,  # упрощение: сам себе мерчант
        amount_original=amount_original,
        currency=data.currency,
        amount_usdt=amount_usdt,
        status=ApplicationStatus.created,
    )
    db.add(app)
    await db.commit()
    await db.refresh(app)
    return app


async def list_applications(db: AsyncSession, user_id: int) -> List[Application]:
    """Список заявок текущего пользователя"""
    res = await db.execute(
        select(Application)
        .where(Application.user_id == user_id)
        .order_by(Application.id.desc())
    )
    return res.scalars().all()


async def confirm_application(db: AsyncSession, user_id: int, app_id: int) -> Application:
    """Подтверждение заявки: ставим approved, считаем комиссию, обновляем баланс"""
    res = await db.execute(
        select(Application).where(
            Application.id == app_id,
            Application.user_id == user_id,
        )
    )
    app = res.scalar_one_or_none()
    if not app:
        raise HTTPException(404, "Application not found")
    if app.status == ApplicationStatus.approved:
        return app
    if app.status == ApplicationStatus.cancelled:
        raise HTTPException(400, "Application already cancelled")

    # комиссия 1.5%
    commission = (
        (Decimal(app.amount_usdt) * COMMISSION_PCT / Decimal(100))
        .quantize(Q6, rounding=ROUND_HALF_UP)
    )
    app.commission_usdt = commission
    app.status = ApplicationStatus.approved

    # обновляем баланс юзера
    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one()
    if user is None:
        raise HTTPException(404, "User not found")

    before_balance = Decimal(user.balance_usdt or 0)
    delta = Decimal(app.amount_usdt) - commission
    after_balance = before_balance + delta

    user.balance_usdt = after_balance

    # создаём запись в истории балансов
    txn = BalanceTransaction(
        user_id=user.id,
        delta_usdt=delta,
        balance_before=before_balance,
        balance_after=after_balance,
        reason="application_approved",
    )
    db.add(txn)

    await db.commit()
    await db.refresh(app)
    return app


async def cancel_application(db: AsyncSession, user_id: int, app_id: int) -> Application:
    """Отмена заявки (если не approved)"""
    res = await db.execute(
        select(Application).where(
            Application.id == app_id,
            Application.user_id == user_id,
        )
    )
    app = res.scalar_one_or_none()
    if not app:
        raise HTTPException(404, "Application not found")
    if app.status == ApplicationStatus.approved:
        raise HTTPException(400, "Already approved, cannot cancel")

    app.status = ApplicationStatus.cancelled
    await db.commit()
    await db.refresh(app)
    return app
