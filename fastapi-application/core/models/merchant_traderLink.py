from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Enum
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .mixins.created_at import CreatedAtMixin
import enum


class LinkStatus(str, enum.Enum):
    active = "active"
    disabled = "disabled"


class MerchantTraderLink(IntIdPkMixin, CreatedAtMixin, Base):
    __tablename__ = "merchant_trader_links"

    merchant_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    trader_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    status: Mapped[LinkStatus] = mapped_column(
        Enum(LinkStatus, name="link_status_enum"), default=LinkStatus.active
    )
    priority: Mapped[int] = mapped_column(Integer, default=100)
    weight: Mapped[int] = mapped_column(Integer, default=1)
    currencies: Mapped[str] = mapped_column(String(128), default="USDT,USD,INR")

    # связи на объекты User
    merchant = relationship(
        "User",
        foreign_keys=[merchant_id],
        backref="merchant_links",
        lazy="joined",
    )
    trader = relationship(
        "User",
        foreign_keys=[trader_id],
        backref="trader_links",
        lazy="joined",
    )
