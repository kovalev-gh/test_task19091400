from pydantic import BaseModel


class RatesRead(BaseModel):
    USD: float = 1.0
    USDT: float = 1.0
    INR: float = 84.0
    RUB: float = 90.0
