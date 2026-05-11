"""add cleanup langchain checkpoints trigger

Revision ID: d2d2faa0f523
Revises: 3cb742728309
Create Date: 2026-05-08 12:59:16.418672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2d2faa0f523'
down_revision: Union[str, Sequence[str], None] = '3cb742728309'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE OR REPLACE FUNCTION cleanup_langchain_checkpoints()
    RETURNS TRIGGER AS $$
    DECLARE
        v_thread_id TEXT;
    BEGIN
        v_thread_id := 'session_' || COALESCE(NEW.id, OLD.id);

        DELETE FROM checkpoint_writes
        WHERE thread_id = v_thread_id;

        DELETE FROM checkpoint_blobs
        WHERE thread_id = v_thread_id;

        DELETE FROM checkpoints
        WHERE thread_id = v_thread_id;

        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # HARD DELETE
    op.execute("""
    CREATE TRIGGER trg_chat_sessions_delete
    AFTER DELETE ON chat_sessions
    FOR EACH ROW
    EXECUTE FUNCTION cleanup_langchain_checkpoints();
    """)

    # SOFT DELETE
    op.execute("""
    CREATE TRIGGER trg_chat_sessions_soft_delete
    AFTER UPDATE OF is_deleted ON chat_sessions
    FOR EACH ROW
    WHEN (
        OLD.is_deleted = false
        AND NEW.is_deleted = true
    )
    EXECUTE FUNCTION cleanup_langchain_checkpoints();
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER IF EXISTS trg_chat_sessions_delete ON chat_sessions;")
    op.execute("DROP TRIGGER IF EXISTS trg_chat_sessions_soft_delete ON chat_sessions;")
    op.execute("DROP FUNCTION IF EXISTS cleanup_langchain_checkpoints();")
