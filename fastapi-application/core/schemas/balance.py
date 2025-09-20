from pydantic import BaseModel


class BalanceRead(BaseModel):
    balance_usdt: float
