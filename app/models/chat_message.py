import uuid
from datetime import datetime

from sqlalchemy import Text, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, ENUM as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.constants.chat import ChatMessageRole
from app.database import Base
# from app.models.chat_session import ChatSession
from app.utils.enum import enum_values

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    # ✅ REQUIRED
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False
    )

    role: Mapped[ChatMessageRole] = mapped_column(
        SQLEnum(ChatMessageRole, name="chat_message_role_enum", values_callable=enum_values),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # ✅ DEFAULT (fix di sini)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        default=None
    )

    intent: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        default=None
    )

    # ✅ RELATIONSHIP terakhir
    session: Mapped["ChatSession"] = relationship(
        "ChatSession",
        back_populates="messages"
    )