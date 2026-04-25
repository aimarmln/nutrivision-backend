from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Boolean,
    Float,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    func
)
from app.database import Base
from app.constants.food_log import MealType
from app.models.food import Food
from app.models.serving import Serving
from app.models.user import User
from app.utils.enum import enum_values


class FoodLog(Base):
    __tablename__ = "food_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        init=False
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    food_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("foods.id"),
        nullable=False
    )

    serving_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('servings.id'),
        nullable=False
    )

    number_of_units: Mapped[float] = mapped_column(Float, nullable=False)

    meal_type: Mapped[MealType] = mapped_column(
        SQLEnum(MealType, name='meal_type_enum', values_callable=enum_values),
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", backref="food_logs", init=False)
    food: Mapped["Food"] = relationship("Food", backref="food_logs", init=False)
    serving: Mapped["Serving"] = relationship("Serving", backref="food_logs", init=False)

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
