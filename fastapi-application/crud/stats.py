from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from core.models import Application
from core.models.application import ApplicationStatus


async def get_stats_overview(db: AsyncSession, days: int = 7):
    """Агрегаты по заявкам за последние N дней"""
    since = datetime.utcnow() - timedelta(days=days)

    # количество по статусам
    stmt_counts = (
        select(Application.status, func.count())
        .where(Application.created_at >= since)
        .group_by(Application.status)
    )
    res_counts = await db.execute(stmt_counts)
    by_status = {status.value if isinstance(status, ApplicationStatus) else status: count
                 for status, count in res_counts.all()}

    # суммарный оборот
    stmt_turnover = select(func.sum(Application.amount_usdt)).where(Application.created_at >= since)
    res_turnover = await db.execute(stmt_turnover)
    total_turnover = res_turnover.scalar() or 0

    # суммарная комиссия
    stmt_commission = select(func.sum(Application.commission_usdt)).where(Application.created_at >= since)
    res_commission = await db.execute(stmt_commission)
    total_commission = res_commission.scalar() or 0

    return {
        "by_status": by_status,
        "total_turnover_usdt": total_turnover,
        "total_commission_usdt": total_commission,
    }
