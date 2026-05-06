"""atuaalizar models lembrete

Revision ID: e2d19cfcc17c
Revises: 7dcd2bb3d915
Create Date: 2026-05-01 19:35:16.948406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2d19cfcc17c'
down_revision: Union[str, Sequence[str], None] = '7dcd2bb3d915'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
