from uuid import UUID
from pydantic import BaseModel, Field
from typing import List
from app.constants.food_log import MealType

class CreateFoodLogSchema(BaseModel):
    food_id: UUID
    serving_id: UUID
    number_of_units: float = Field(gt=0)
    meal_type: MealType

class UpdateFoodLogSchema(BaseModel):
    serving_id: UUID
    number_of_units: float = Field(gt=0)

class BulkUpdateFoodLogItem(BaseModel):
    id: UUID
    serving_id: UUID
    number_of_units: float = Field(gt=0)

class BulkUpdateFoodLogSchema(BaseModel):
    updates: List[BulkUpdateFoodLogItem] = Field(min_length=1)

class BulkAddFoodLogSchema(BaseModel):
    items: list[CreateFoodLogSchema] = Field(min_length=1)