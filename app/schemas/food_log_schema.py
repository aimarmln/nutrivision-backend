from uuid import UUID
from pydantic import BaseModel
from app.constants.food_log import MealType

class CreateFoodLogSchema(BaseModel):
    food_id: UUID
    serving_id: UUID
    number_of_units: float
    meal_type: MealType

class UpdateFoodLogSchema(BaseModel):
    serving_id: UUID
    number_of_units: float