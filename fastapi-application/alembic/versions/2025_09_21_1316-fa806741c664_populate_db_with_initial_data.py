"""populate db with initial data

Revision ID: fa806741c664
Revises: d249ec50779d
Create Date: 2025-09-21 13:16:04.226895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import bcrypt

# revision identifiers, used by Alembic.
revision: str = "fa806741c664"
down_revision: Union[str, None] = "d249ec50779d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # bcrypt-хэши паролей
    def hash_password(pw: str) -> str:
        return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # --- USERS ---
    conn.execute(
        sa.text(
            """
            INSERT INTO users (id, username, email, hashed_password, role, balance_usdt, created_at)
            VALUES (:id, :username, :email, :hashed_password, :role, :balance_usdt, now())
            """
        ),
        [
            {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "hashed_password": hash_password("admin"),
                "role": "admin",
                "balance_usdt": 0,
            },
            {
                "id": 2,
                "username": "merchant1",
                "email": "merchant1@example.com",
                "hashed_password": hash_password("merchant"),
                "role": "merchant",
                "balance_usdt": 1000,
            },
            {
                "id": 3,
                "username": "trader1",
                "email": "trader1@example.com",
                "hashed_password": hash_password("trader"),
                "role": "trader",
                "balance_usdt": 500,
            },
        ],
    )

    # --- APPLICATIONS ---
    conn.execute(
        sa.text(
            """
            INSERT INTO applications (id, user_id, merchant_id, trader_id,
                amount_original, currency, amount_usdt, commission_usdt, status, created_at)
            VALUES (:id, :user_id, :merchant_id, :trader_id,
                :amount_original, :currency, :amount_usdt, :commission_usdt, :status, now())
            """
        ),
        [
            {
                "id": 1,
                "user_id": 2,
                "merchant_id": 2,
                "trader_id": 3,
                "amount_original": 100,
                "currency": "USD",
                "amount_usdt": 99.5,
                "commission_usdt": 0.5,
                "status": "created",
            },
            {
                "id": 2,
                "user_id": 3,
                "merchant_id": 2,
                "trader_id": 3,
                "amount_original": 200,
                "currency": "EUR",
                "amount_usdt": 198,
                "commission_usdt": 2,
                "status": "approved",
            },
        ],
    )

    # --- BALANCE TRANSACTIONS ---
    conn.execute(
        sa.text(
            """
            INSERT INTO balance_transactions
                (id, user_id, delta_usdt, reason, balance_before, balance_after, created_at)
            VALUES (:id, :user_id, :delta_usdt, :reason, :balance_before, :balance_after, now())
            """
        ),
        [
            {
                "id": 1,
                "user_id": 2,
                "delta_usdt": 1000,
                "reason": "Initial deposit",
                "balance_before": 0,
                "balance_after": 1000,
            },
            {
                "id": 2,
                "user_id": 3,
                "delta_usdt": 500,
                "reason": "Initial deposit",
                "balance_before": 0,
                "balance_after": 500,
            },
        ],
    )

    # --- MERCHANT ↔ TRADER LINKS ---
    conn.execute(
        sa.text(
            """
            INSERT INTO merchant_trader_links
                (id, merchant_id, trader_id, status, priority, weight, currencies, created_at)
            VALUES (:id, :merchant_id, :trader_id, :status, :priority, :weight, :currencies, now())
            """
        ),
        [
            {
                "id": 1,
                "merchant_id": 2,
                "trader_id": 3,
                "status": "active",
                "priority": 1,
                "weight": 10,
                "currencies": "USD,EUR",
            }
        ],
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM merchant_trader_links"))
    conn.execute(sa.text("DELETE FROM balance_transactions"))
    conn.execute(sa.text("DELETE FROM applications"))
    conn.execute(
        sa.text(
            "DELETE FROM users WHERE username in ('admin','merchant1','trader1')"
        )
    )
