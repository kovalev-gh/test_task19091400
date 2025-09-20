from pydantic import BaseModel
from decimal import Decimal
from typing import Dict


class StatsOverview(BaseModel):
    by_status: Dict[str, int]
    total_turnover_usdt: Decimal
    total_commission_usdt: Decimal
