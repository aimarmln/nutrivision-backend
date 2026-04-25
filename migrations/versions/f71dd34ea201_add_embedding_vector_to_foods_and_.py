"""add embedding vector to foods and recipes

Revision ID: f71dd34ea201
Revises: e8275cb76473
Create Date: 2026-04-16 10:24:46.159990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = 'f71dd34ea201'
down_revision: Union[str, Sequence[str], None] = 'e8275cb76473'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # =========================
    # ENABLE EXTENSION
    # =========================
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # =========================
    # ADD EMBEDDING COLUMNS
    # =========================
    op.add_column(
        "foods",
        sa.Column("embedding", Vector(768), nullable=True)
    )

    op.add_column(
        "servings",
        sa.Column("embedding", Vector(768), nullable=True)
    )

    op.add_column(
        "recipes",
        sa.Column("embedding", Vector(768), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""

    # =========================
    # DROP COLUMNS
    # =========================
    op.drop_column("recipes", "embedding")
    op.drop_column("servings", "embedding")
    op.drop_column("foods", "embedding")
