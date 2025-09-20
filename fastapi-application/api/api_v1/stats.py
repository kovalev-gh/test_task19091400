from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper
from core.schemas.stats import StatsOverview
from crud import stats as crud_stats
from core.auth import get_current_user

#router = APIRouter(prefix="/api/v1/stats", tags=["Stats"])
router = APIRouter()

@router.get("/overview", response_model=StatsOverview)
async def stats_overview(
    days: int = Query(7, ge=1, le=365),
    db: AsyncSession = Depends(db_helper.session_getter),
    user=Depends(get_current_user),
):
    """Агрегаты по заявкам за последние N дней"""
    return await crud_stats.get_stats_overview(db, days=days)
