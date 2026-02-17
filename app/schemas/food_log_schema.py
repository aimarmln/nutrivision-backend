from uuid import UUID
from pydantic import BaseModel
from app.constants.food_log import MealType

class CreateFoodLogSchema(BaseModel):
    food_id: UUID
    meal_type: MealType
    weight_grams: float

class UpdateFoodLogSchema(BaseModel):
    weight_grams: float