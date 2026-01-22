"""merge multiple heads

Revision ID: c86a2d9c8ae1
Revises: 2f07ef838c55, 9f2a1c3d4e5f
Create Date: 2026-01-21 21:40:36.586806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c86a2d9c8ae1'
down_revision: Union[str, Sequence[str], None] = ('2f07ef838c55', '9f2a1c3d4e5f')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
