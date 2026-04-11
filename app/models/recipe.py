import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String,
    Integer,
    Float,
    Text,
    DateTime,
    Boolean,
    Enum as SQLEnum,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.constants.recipe import HealthCategory
from app.utils.enum import enum_values

class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    ingredients: Mapped[str] = mapped_column(Text, nullable=False)
    instructions: Mapped[str] = mapped_column(Text, nullable=False)

    serving_yield: Mapped[int] = mapped_column(Integer, nullable=False)

    calories_per_serving_kcal: Mapped[float] = mapped_column(Float, nullable=False)
    fat_per_serving_g: Mapped[float] = mapped_column(Float, nullable=False)
    cholesterol_per_serving_mg: Mapped[float] = mapped_column(Float, nullable=False)
    protein_per_serving_g: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrate_per_serving_g: Mapped[float] = mapped_column(Float, nullable=False)
    fiber_per_serving_g: Mapped[float] = mapped_column(Float, nullable=False)
    sugar_per_serving_g: Mapped[float] = mapped_column(Float, nullable=False)
    sodium_per_serving_mg: Mapped[float] = mapped_column(Float, nullable=False)
    kalium_per_serving_mg: Mapped[float] = mapped_column(Float, nullable=False)

    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    health_category: Mapped[HealthCategory] = mapped_column(
        SQLEnum(HealthCategory, name="health_category_enum", values_callable=enum_values), nullable=False
    )

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
