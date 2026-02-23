import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Float,  Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Serving(Base):
    __tablename__ = 'servings'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    food_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('foods.id', ondelete='CASCADE'),
        nullable=False
    )

    serving_unit: Mapped[str] = mapped_column(String(100), nullable=False)
    number_of_units: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    calories_kcal: Mapped[float] = mapped_column(Float, nullable=False)
    fat_g: Mapped[float] = mapped_column(Float, nullable=False)
    cholesterol_mg: Mapped[float] = mapped_column(Float, nullable=False)
    protein_g: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrate_g: Mapped[float] = mapped_column(Float, nullable=False)
    fiber_g: Mapped[float] = mapped_column(Float, nullable=False)
    sugar_g: Mapped[float] = mapped_column(Float, nullable=False)
    sodium_mg: Mapped[float] = mapped_column(Float, nullable=False)
    kalium_mg: Mapped[float] = mapped_column(Float, nullable=False)

    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

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
