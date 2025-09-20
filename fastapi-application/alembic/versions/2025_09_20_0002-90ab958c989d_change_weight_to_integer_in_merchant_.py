"""change weight to Integer in merchant_trader_links

Revision ID: 90ab958c989d
Revises: 6401a9f62787
Create Date: 2025-09-20 00:02:54.593218
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "90ab958c989d"
down_revision: Union[str, None] = "6401a9f62787"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- создаём новый enum ---
    new_enum = sa.Enum("active", "disabled", name="link_status_enum")
    new_enum.create(op.get_bind(), checkfirst=True)

    # меняем колонку status на новый enum через CAST
    op.execute(
        "ALTER TABLE merchant_trader_links "
        "ALTER COLUMN status TYPE link_status_enum "
        "USING status::text::link_status_enum"
    )

    # меняем weight на Integer
    op.alter_column(
        "merchant_trader_links",
        "weight",
        existing_type=sa.Numeric(5, 2),
        type_=sa.Integer(),
        existing_nullable=False,
    )

    # удаляем старый enum
    op.execute("DROP TYPE IF EXISTS linkstatus")


def downgrade() -> None:
    # создаём старый enum
    old_enum = postgresql.ENUM("active", "disabled", name="linkstatus")
    old_enum.create(op.get_bind(), checkfirst=True)

    # возвращаем колонку status на старый enum через CAST
    op.execute(
        "ALTER TABLE merchant_trader_links "
        "ALTER COLUMN status TYPE linkstatus "
        "USING status::text::linkstatus"
    )

    # возвращаем weight обратно в Numeric
    op.alter_column(
        "merchant_trader_links",
        "weight",
        existing_type=sa.Integer(),
        type_=sa.Numeric(5, 2),
        existing_nullable=False,
    )

    # удаляем новый enum
    op.execute("DROP TYPE IF EXISTS link_status_enum")
