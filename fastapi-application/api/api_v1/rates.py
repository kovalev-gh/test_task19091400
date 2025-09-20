from fastapi import APIRouter
from core.schemas.rates import RatesRead

#router = APIRouter(tags=["Rates"])
router = APIRouter()
@router.get("/rates", response_model=RatesRead)
async def get_rates():
    # мок-курсы согласно ТЗ, база USDT=1
    return {"USD": 1.0, "USDT": 1.0, "INR": 84.0, "RUB": 90.0}
