import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # ✅ RELATIONSHIP (harus sebelum default)
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    # ✅ DEFAULT
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        default=None
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        default=None
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    title: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        default=None
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None
    )