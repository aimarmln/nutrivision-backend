"""add hnsw index to embeddings

Revision ID: 3cb742728309
Revises: f71dd34ea201
Create Date: 2026-04-16 11:34:14.438118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3cb742728309'
down_revision: Union[str, Sequence[str], None] = 'f71dd34ea201'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    # =========================
    # CREATE HNSW INDEXES
    # =========================

    # foods
    op.execute("""
        CREATE INDEX foods_embedding_hnsw_idx
        ON foods
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """)

    # servings (PALING PENTING)
    op.execute("""
        CREATE INDEX servings_embedding_hnsw_idx
        ON servings
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """)

    # recipes
    op.execute("""
        CREATE INDEX recipes_embedding_hnsw_idx
        ON recipes
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """)


def downgrade() -> None:
    """Downgrade schema."""
    
     # =========================
    # DROP INDEXES
    # =========================
    op.execute("DROP INDEX IF EXISTS recipes_embedding_hnsw_idx;")
    op.execute("DROP INDEX IF EXISTS servings_embedding_hnsw_idx;")
    op.execute("DROP INDEX IF EXISTS foods_embedding_hnsw_idx;")
