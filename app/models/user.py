import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Boolean, Date, DateTime, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from app.constants.user import Gender, ActivityLevel, MainGoal, BMIStatus, UserStatus
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

    name: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)

    gender: Mapped[Gender | None] = mapped_column(SQLEnum(Gender, name='gender_enum', values_callable=enum_values), nullable=True, default=None)

    birthday: Mapped[datetime | None] = mapped_column(Date, nullable=True, default=None)

    age: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)

    height_cm: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    weight_kg: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)

    activity_level: Mapped[ActivityLevel | None] = mapped_column(
        SQLEnum(ActivityLevel, name='activity_level_enum', values_callable=enum_values),
        nullable=True,
        default=None
    )   

    main_goal: Mapped[MainGoal | None] = mapped_column(
        SQLEnum(MainGoal, name='main_goal_enum', values_callable=enum_values),
        nullable=True,
        default=None
    )

    bmr: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)

    bmi: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)

    bmi_status: Mapped[BMIStatus | None] = mapped_column(
        SQLEnum(BMIStatus, name='bmi_status_enum', values_callable=enum_values),
        nullable=True,
        default=None
    )

    calories_per_day_kcal: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    carbohydrates_per_day_g: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    proteins_per_day_g: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)
    fats_per_day_g: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)

    status: Mapped[UserStatus] = mapped_column(
        SQLEnum(UserStatus, name='user_status_enum', values_callable=enum_values),
        nullable=False,
        default=UserStatus.DRAFT
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
