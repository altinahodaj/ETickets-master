"""add photos table

Revision ID: 9f2a1c3d4e5f
Revises: 6bcd50c8ca87
Create Date: 2026-01-20

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f2a1c3d4e5f"
down_revision: Union[str, Sequence[str], None] = "6bcd50c8ca87"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "photos",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("cinema_id", sa.Integer(), nullable=True),
        sa.Column("movie_id", sa.Integer(), nullable=True),
        sa.Column("photo_type", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("img_path", sa.String(length=500), nullable=False),
        sa.Column("img_client_path", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.Column("insert_date", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["cinema_id"], ["cinemas.id"]),
        sa.ForeignKeyConstraint(["movie_id"], ["movies.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("photos")
