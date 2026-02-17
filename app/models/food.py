import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String,
    Integer,
    Float,
    DateTime,
    Boolean,
    func
)
from sqlalchemy import (
    String,
    Float,
    Integer,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Food(Base):
    __tablename__ = "foods"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    yolo_label: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)

    calories_per_100g_kcal: Mapped[float] = mapped_column(Float, nullable=False)
    fat_per_100g_g: Mapped[float] = mapped_column(Float, nullable=False)
    cholesterol_per_100g_mg: Mapped[float] = mapped_column(Float, nullable=False)
    protein_per_100g_g: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrate_per_100g_g: Mapped[float] = mapped_column(Float, nullable=False)
    fiber_per_100g_g: Mapped[float] = mapped_column(Float, nullable=False)
    sugar_per_100g_g: Mapped[float] = mapped_column(Float, nullable=False)
    sodium_per_100g_mg: Mapped[float] = mapped_column(Float, nullable=False)
    kalium_per_100g_mg: Mapped[float] = mapped_column(Float, nullable=False)

    instance_weight_g: Mapped[int | None] = mapped_column(Integer, nullable=True)

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
