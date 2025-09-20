from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Literal


class LinkBase(BaseModel):
    merchant_id: int
    trader_id: int
    status: Literal["active", "disabled"] = "active"
    priority: int = 100
    weight: int = 1
    currencies: str = "USDT,USD,INR"


class LinkCreate(LinkBase):
    pass


class LinkUpdate(BaseModel):
    status: Literal["active", "disabled"] | None = None
    priority: int | None = None
    weight: int | None = None
    currencies: str | None = None


class LinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    merchant_id: int
    trader_id: int
    status: str
    priority: int
    weight: int
    currencies: str
    created_at: datetime
