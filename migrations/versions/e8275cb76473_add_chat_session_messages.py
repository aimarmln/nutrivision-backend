"""add chat session messages

Revision ID: e8275cb76473
Revises: 0ceace46c2dd
Create Date: 2026-04-12 21:36:51.279593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e8275cb76473'
down_revision: Union[str, Sequence[str], None] = '0ceace46c2dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # =========================
    # ENUM
    # =========================
    op.execute("""
        CREATE TYPE chat_message_role_enum AS ENUM ('User', 'Assistant')
    """)

    # =========================
    # CHAT SESSIONS (TIMEOUT BASED)
    # =========================
    op.create_table(
        "chat_sessions",
        sa.Column(
            "id",
            sa.Integer,
            primary_key=True,
            autoincrement=True
        ),

        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False
        ),

        # # AI generated title for the session, can be null for ongoing sessions without a title yet
        # sa.Column("title", sa.String(150), nullable=True),

        sa.Column(
            "last_activity_at",
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False
        ),

        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, nullable=True),
        sa.Column("deleted_at", sa.DateTime, nullable=True)
    )

    # =========================
    # CHAT MESSAGES
    # =========================
    op.create_table(
        "chat_messages",
        sa.Column(
            "id",
            sa.Integer,
            primary_key=True,
            autoincrement=True
        ),

        sa.Column(
            "session_id",
            sa.Integer,
            sa.ForeignKey("chat_sessions.id", ondelete="CASCADE"),
            nullable=False
        ),

        sa.Column("role", postgresql.ENUM("User", "Assistant", name="chat_message_role_enum", create_type=False), nullable=False),

        sa.Column("message", sa.Text, nullable=False),

        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False
        ),
    )

    # =========================
    # INDEXES (IMPORTANT FOR PERFORMANCE)
    # =========================

    # sessions: user chat listing + timeout
    op.create_index(
        "idx_chat_sessions_user_active",
        "chat_sessions",
        ["user_id", "is_deleted"]
    )

    op.create_index(
        "idx_chat_sessions_last_activity",
        "chat_sessions",
        ["last_activity_at"]
    )

    # messages: fast history loading
    op.create_index(
        "idx_chat_messages_session",
        "chat_messages",
        ["session_id"]
    )

    op.create_index(
        "idx_chat_messages_created_at",
        "chat_messages",
        ["created_at"]
    )

    op.create_index(
        "idx_chat_messages_session_role_created",
        "chat_messages",
        ["session_id", "role", "created_at"]
    )


def downgrade() -> None:
    # drop indexes
    op.drop_index("idx_chat_messages_session_role_created", table_name="chat_messages")
    op.drop_index("idx_chat_messages_created_at", table_name="chat_messages")
    op.drop_index("idx_chat_messages_session", table_name="chat_messages")

    op.drop_index("idx_chat_sessions_last_activity", table_name="chat_sessions")
    op.drop_index("idx_chat_sessions_user_active", table_name="chat_sessions")

    # drop tables
    op.drop_table("chat_messages")
    op.drop_table("chat_sessions")

    # drop enum
    op.execute("DROP TYPE chat_message_role_enum")
