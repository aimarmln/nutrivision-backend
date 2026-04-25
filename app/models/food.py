import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Boolean, func
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from app.database import Base

if TYPE_CHECKING:
    from app.models.serving import Serving

class Food(Base):
    __tablename__ = "foods"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    yolo_label: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)

    category: Mapped[str] = mapped_column(String(50), nullable=False)
    subcategory: Mapped[str] = mapped_column(String(50), nullable=True)

    # Will be populated by a trigger in the database, not directly by SQLAlchemy
    search_vector: Mapped[str] = mapped_column(TSVECTOR, nullable=True) 

    # Relationships
    servings: Mapped[list["Serving"]] = relationship("Serving", back_populates="food")

    embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True, default=None)

    # Audit fields
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now()
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
