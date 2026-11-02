"""add balance check

Revision ID: 15ed57f7a5e4
Revises: a43be706f6ec
Create Date: 2026-11-02 11:29:47.076899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15ed57f7a5e4'
down_revision: Union[str, Sequence[str], None] = 'a43be706f6ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint(
        "ck_wallets_balance_non_negative", "wallets", "wallet_balance >= 0"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("ck_wallets_balance_non_negative", "wallets", type_="check")
