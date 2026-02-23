"""add full text search to foods

Revision ID: 0ceace46c2dd
Revises: 559733462727
Create Date: 2026-02-23 15:31:01.722196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ceace46c2dd'
down_revision: Union[str, Sequence[str], None] = '559733462727'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create function
    op.execute("""
        CREATE FUNCTION food_search_vector_update() RETURNS trigger AS $$
        BEGIN
          NEW.search_vector :=
            setweight(to_tsvector('simple', coalesce(NEW.name, '')), 'A') ||
            setweight(to_tsvector('simple', coalesce(NEW.category, '')), 'B') ||
            setweight(to_tsvector('simple', coalesce(NEW.subcategory, '')), 'C');
          RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
    """)

    # Create trigger
    op.execute("""
        CREATE TRIGGER food_search_vector_trigger
        BEFORE INSERT OR UPDATE
        ON foods
        FOR EACH ROW
        EXECUTE FUNCTION food_search_vector_update();
    """)

    # Backfill existing rows
    op.execute("""
        UPDATE foods SET
            search_vector =
                setweight(to_tsvector('simple', coalesce(name, '')), 'A') ||
                setweight(to_tsvector('simple', coalesce(category, '')), 'B') ||
                setweight(to_tsvector('simple', coalesce(subcategory, '')), 'C');
    """)

    # Create GIN index
    op.execute("""
        CREATE INDEX food_search_idx
        ON foods
        USING GIN (search_vector);
    """)


def downgrade() -> None:
    """Downgrade schema."""
    
    op.execute("DROP INDEX IF EXISTS food_search_idx;")
    op.execute("DROP TRIGGER IF EXISTS food_search_vector_trigger ON foods;")
    op.execute("DROP FUNCTION IF EXISTS food_search_vector_update;")
    