from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Numeric, Enum, ForeignKey
from decimal import Decimal
import enum

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .mixins.created_at import CreatedAtMixin


class ApplicationStatus(str, enum.Enum):
    created = "created"
    approved = "approved"
    cancelled = "cancelled"


class Application(IntIdPkMixin, CreatedAtMixin, Base):
    __tablename__ = "applications"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    merchant_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    trader_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)

    amount_original: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    currency: Mapped[str] = mapped_column(String(8))
    amount_usdt: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    commission_usdt: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=0)

    status: Mapped[ApplicationStatus] = mapped_column(Enum(ApplicationStatus), default=ApplicationStatus.created)
