from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Integer, Text, DateTime, Enum as SQLEnum, ForeignKey, func
from app.database import Base
from app.constants.comment import Sentiment
from app.models.user import User
from app.models.recipe import Recipe
from app.utils.enum import enum_values

class Comment(Base):
    __tablename__ = "comments"
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        init=False
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    recipe_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False
    )

    text: Mapped[str] = mapped_column(Text, nullable=False)

    sentiment: Mapped[Sentiment] = mapped_column(
        SQLEnum(Sentiment, name="sentiment_enum", values_callable=enum_values),
        nullable=False
    )

     # Relationships
    user: Mapped["User"] = relationship("User", backref="comments", init=False)
    recipe: Mapped["Recipe"] = relationship("Recipe", backref="comments", init=False)

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

