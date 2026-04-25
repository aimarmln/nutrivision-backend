from datetime import datetime
from typing import TYPE_CHECKING
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Float,  Boolean, DateTime, func
from app.database import Base

if TYPE_CHECKING:
    from app.models.food import Food


class Serving(Base):
    __tablename__ = 'servings'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    food_id: Mapped[int] = mapped_column(
        Integer,
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

    food: Mapped["Food"] = relationship(
        "Food",
        back_populates="servings"
    )

    embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True, default=None)

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
