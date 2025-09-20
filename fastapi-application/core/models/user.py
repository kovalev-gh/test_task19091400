from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, Numeric
from decimal import Decimal
import enum

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .mixins.created_at import CreatedAtMixin


class UserRole(str, enum.Enum):
    merchant = "merchant"
    trader = "trader"
    admin = "admin"


class User(IntIdPkMixin, CreatedAtMixin, Base):
    __tablename__ = "users"
    hashed_password: Mapped[str]
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.merchant)

    balance_usdt: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=0)

    @property
    def email(self) -> str:
        return f"{self.username}@domain.com"