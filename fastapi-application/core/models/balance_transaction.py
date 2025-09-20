from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, ForeignKey
from decimal import Decimal

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .mixins.created_at import CreatedAtMixin


class BalanceTransaction(IntIdPkMixin, CreatedAtMixin, Base):
    __tablename__ = "balance_transactions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    delta_usdt: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    reason: Mapped[str] = mapped_column(String(64))

    # поля истории баланса
    balance_before: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    balance_after: Mapped[Decimal] = mapped_column(Numeric(18, 6))
