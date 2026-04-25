from datetime import datetime
from sqlalchemy import Integer, Text, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import ENUM as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.constants.chat import ChatMessageRole
from app.database import Base
from app.utils.enum import enum_values
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.chat_session import ChatSession

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    # ✅ REQUIRED
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    session_id: Mapped[int] = mapped_column(
        Integer,
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

    session: Mapped["ChatSession"] = relationship(
        "ChatSession",
        back_populates="messages"
    )