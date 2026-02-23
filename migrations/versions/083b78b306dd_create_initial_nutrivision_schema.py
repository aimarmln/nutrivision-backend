"""create initial nutrivision schema

Revision ID: 083b78b306dd
Revises: 
Create Date: 2026-02-16 19:02:10.138346

"""
import uuid
import sqlalchemy as sa
from typing import Sequence, Union
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '083b78b306dd'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    # # =========================
    # # ENUM TYPES
    # # =========================
    op.execute("CREATE TYPE user_status_enum AS ENUM ('Active', 'Draft')")
    op.execute("CREATE TYPE gender_enum AS ENUM ('Male', 'Female')")
    op.execute("CREATE TYPE activity_level_enum AS ENUM ('Sedentary', 'Lightly Active', 'Moderately Active', 'Active', 'Very Active')")
    op.execute("CREATE TYPE main_goal_enum AS ENUM ('Lose Weight', 'Maintain Weight', 'Gain Weight')")
    op.execute("CREATE TYPE bmi_status_enum AS ENUM ('Underweight', 'Healthy', 'Overweight', 'Obesity Class I', 'Obesity Class II')")
    op.execute("CREATE TYPE meal_type_enum AS ENUM ('Breakfast', 'Lunch', 'Dinner', 'Snack')")
    op.execute("CREATE TYPE health_category_enum AS ENUM ('Healthy', 'Unhealthy')")
    op.execute("CREATE TYPE sentiment_enum AS ENUM ('Positive', 'Negative')")

    # =========================
    # USERS TABLE
    # =========================
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("status", postgresql.ENUM("Active", "Draft", name="user_status_enum", create_type=False), nullable=False, server_default="Draft"),
        sa.Column("name", sa.String(100)),
        sa.Column("gender", postgresql.ENUM("Male", "Female", name="gender_enum", create_type=False)),
        sa.Column("birthday", sa.Date),
        sa.Column("age", sa.Integer),
        sa.Column("height_cm", sa.Integer),
        sa.Column("weight_kg", sa.Integer),
        sa.Column("activity_level", postgresql.ENUM("Sedentary", "Lightly Active", "Moderately Active", "Active", "Very Active", name="activity_level_enum", create_type=False)),
        sa.Column("main_goal", postgresql.ENUM("Lose Weight", "Maintain Weight", "Gain Weight", name="main_goal_enum", create_type=False)),
        sa.Column("bmr", sa.Float),
        sa.Column("bmi", sa.Float),
        sa.Column("bmi_status", postgresql.ENUM("Underweight", "Healthy", "Overweight", "Obesity Class I", "Obesity Class II", name="bmi_status_enum", create_type=False)),
        sa.Column("calories_per_day_kcal", sa.Integer),
        sa.Column("carbohydrates_per_day_g", sa.Float),
        sa.Column("proteins_per_day_g", sa.Float),
        sa.Column("fats_per_day_g", sa.Float),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("deleted_at", sa.DateTime),
    )


    # =========================
    # FOODS TABLE
    # =========================
    op.create_table(
        "foods",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("yolo_label", sa.String(50), unique=True),
        sa.Column("calories_per_100g_kcal", sa.Float, nullable=False),
        sa.Column("fat_per_100g_g", sa.Float, nullable=False),
        sa.Column("cholesterol_per_100g_mg", sa.Float, nullable=False),
        sa.Column("protein_per_100g_g", sa.Float, nullable=False),
        sa.Column("carbohydrate_per_100g_g", sa.Float, nullable=False),
        sa.Column("fiber_per_100g_g", sa.Float, nullable=False),
        sa.Column("sugar_per_100g_g", sa.Float, nullable=False),
        sa.Column("sodium_per_100g_mg", sa.Float, nullable=False),
        sa.Column("kalium_per_100g_mg", sa.Float, nullable=False),
        sa.Column("instance_weight_g", sa.Integer),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("deleted_at", sa.DateTime),
    )


    # =========================
    # RECIPES TABLE
    # =========================
    op.create_table(
        "recipes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("ingredients", sa.Text, nullable=False),
        sa.Column("instructions", sa.Text, nullable=False),
        sa.Column("serving_yield", sa.Integer, nullable=False),
        sa.Column("calories_per_serving_kcal", sa.Float, nullable=False),
        sa.Column("fat_per_serving_g", sa.Float, nullable=False),
        sa.Column("cholesterol_per_serving_mg", sa.Float, nullable=False),
        sa.Column("protein_per_serving_g", sa.Float, nullable=False),
        sa.Column("carbohydrate_per_serving_g", sa.Float, nullable=False),
        sa.Column("fiber_per_serving_g", sa.Float, nullable=False),
        sa.Column("sugar_per_serving_g", sa.Float, nullable=False),
        sa.Column("sodium_per_serving_mg", sa.Float, nullable=False),
        sa.Column("kalium_per_serving_mg", sa.Float, nullable=False),
        sa.Column("image_url", sa.String(255)),
        sa.Column("health_category", postgresql.ENUM("Healthy", "Unhealthy", name="health_category_enum", create_type=False), nullable=False),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("deleted_at", sa.DateTime),
    )


    # =========================
    # FOOD LOGS TABLE
    # =========================
    op.create_table(
        "food_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("food_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("foods.id"), nullable=False),
        sa.Column("meal_type", postgresql.ENUM("Breakfast", "Lunch", "Dinner", "Snack", name="meal_type_enum", create_type=False), nullable=False),
        sa.Column("weight_grams", sa.Float, nullable=False),
        sa.Column("calories", sa.Float, nullable=False),
        sa.Column("carbohydrates", sa.Float, nullable=False),
        sa.Column("proteins", sa.Float, nullable=False),
        sa.Column("fats", sa.Float, nullable=False),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("deleted_at", sa.DateTime),
    )


    # =========================
    # COMMENTS TABLE
    # =========================
    op.create_table(
        "comments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("recipe_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("recipes.id"), nullable=False),
        sa.Column("text", sa.Text, nullable=False),
        sa.Column("sentiment", postgresql.ENUM("Positive", "Negative", "Neutral", name="sentiment_enum", create_type=False), nullable=False),
        sa.Column("is_deleted", sa.Boolean, nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("deleted_at", sa.DateTime),
    )


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_table("comments")
    op.drop_table("food_logs")
    op.drop_table("recipes")
    op.drop_table("foods")
    op.drop_table("users")

    op.execute("DROP TYPE sentiment_enum")
    op.execute("DROP TYPE health_category_enum")
    op.execute("DROP TYPE meal_type_enum")
    op.execute("DROP TYPE bmi_status_enum")
    op.execute("DROP TYPE main_goal_enum")
    op.execute("DROP TYPE activity_level_enum")
    op.execute("DROP TYPE gender_enum")
    op.execute("DROP TYPE user_status_enum")
