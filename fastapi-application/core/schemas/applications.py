from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import Literal


# Базовая часть (для создания)
class ApplicationBase(BaseModel):
    amount_original: Decimal
    currency: Literal["USDT", "USD", "INR", "RUB"]


# Для POST /applications
class ApplicationCreate(ApplicationBase):
    pass


# Для возврата (GET /applications и при подтверждении/отмене)
class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    merchant_id: int | None = None
    trader_id: int | None = None
    amount_original: Decimal
    currency: str
    amount_usdt: Decimal
    commission_usdt: Decimal | None = None
    status: str
    created_at: datetime


# Для подтверждения заявки
class ApplicationConfirm(BaseModel):
    id: int


# Для отмены заявки
class ApplicationCancel(BaseModel):
    id: int
