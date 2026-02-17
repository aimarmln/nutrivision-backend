import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Boolean,
    Float,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.constants.food_log import MealType
from app.models.food import Food
from app.models.user import User
from app.utils.enum import enum_values


class FoodLog(Base):
    __tablename__ = "food_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    food_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("foods.id"),
        nullable=False
    )

    meal_type: Mapped[MealType] = mapped_column(
        SQLEnum(MealType, name='meal_type_enum', values_callable=enum_values),
        nullable=False
    )

    weight_grams: Mapped[float] = mapped_column(Float, nullable=False)

    calories: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrates: Mapped[float] = mapped_column(Float, nullable=False)
    proteins: Mapped[float] = mapped_column(Float, nullable=False)
    fats: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", backref="food_logs")
    food: Mapped["Food"] = relationship("Food", backref="food_logs")

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
