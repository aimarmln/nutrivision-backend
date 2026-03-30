import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Boolean, Date, DateTime, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.constants.user import Gender, ActivityLevel, MainGoal, BMIStatus
from app.utils.enum import enum_values

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    gender: Mapped[Gender] = mapped_column(SQLEnum(Gender, name='gender_enum', values_callable=enum_values), nullable=False)

    birthday: Mapped[datetime] = mapped_column(Date, nullable=False)

    age: Mapped[int] = mapped_column(Integer, nullable=False)

    height_cm: Mapped[int] = mapped_column(Integer, nullable=False)
    weight_kg: Mapped[int] = mapped_column(Integer, nullable=False)

    activity_level: Mapped[ActivityLevel] = mapped_column(
        SQLEnum(ActivityLevel, name='activity_level_enum', values_callable=enum_values),
        nullable=False,

    )   

    main_goal: Mapped[MainGoal] = mapped_column(
        SQLEnum(MainGoal, name='main_goal_enum', values_callable=enum_values),
        nullable=False,

    )

    bmr: Mapped[float] = mapped_column(Float, nullable=False)

    bmi: Mapped[float] = mapped_column(Float, nullable=False)

    bmi_status: Mapped[BMIStatus] = mapped_column(
        SQLEnum(BMIStatus, name='bmi_status_enum', values_callable=enum_values),
        nullable=False,

    )

    calories_per_day_kcal: Mapped[int] = mapped_column(Integer, nullable=False)
    carbohydrates_per_day_g: Mapped[float] = mapped_column(Float, nullable=False)
    proteins_per_day_g: Mapped[float] = mapped_column(Float, nullable=False)
    fats_per_day_g: Mapped[float] = mapped_column(Float, nullable=False)

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
