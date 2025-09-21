from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user
from core.models import User
from core.models.db_helper import db_helper
from core.schemas.balance import BalanceRead

#router = APIRouter(tags=["Balances"])
router = APIRouter()
@router.get("/balance", response_model=BalanceRead)
async def get_balance(
    claims=Depends(get_current_user),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    res = await db.execute(select(User).where(User.id == claims["user_id"]))
    user = res.scalar_one()
    return {"balance_usdt": float(user.balance_usdt or 0)}
