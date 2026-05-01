from pydantic import BaseModel, Field
from typing import List, Optional
from app.constants.food_log import MealType

class CreateFoodLogSchema(BaseModel):
    food_id: int = Field(gt=0, description="ID makanan dari search_foods")
    serving_id: int = Field(gt=0, description="ID serving dari get_food_servings")
    number_of_units: float = Field(gt=0, description="Jumlah unit yang dikonsumsi user")
    meal_type: MealType = Field(description="Jenis makan: Breakfast, Lunch, Dinner, Snack")

class UpdateFoodLogSchema(BaseModel):
    serving_id: int = Field(gt=0)
    number_of_units: float = Field(gt=0)

class BulkAddFoodLogItem(BaseModel):
    food_id: int = Field(gt=0, description="ID makanan dari search_foods")
    serving_id: int = Field(gt=0, description="ID serving dari get_food_servings")
    number_of_units: float = Field(gt=0, description="Jumlah unit yang dikonsumsi user")
    meal_type: Optional[MealType] = Field(
        default=None,
        description="Jenis makan: Breakfast, Lunch, Dinner, Snack. Optional, isi jika user menyebutkan secara eksplisit"
    )

class BulkUpdateFoodLogItem(BaseModel):
    id: int = Field(
        gt=0,
        description="ID log makanan yang akan diedit, dapatkan dari get_today_food_logs"
    )

    food_id: Optional[int] = Field(
        default=None,
        description="Jika diisi berarti REPLACE makanan (override food lama)"
    )

    serving_id: int = Field(
        gt=0, 
        description="ID serving baru dari get_food_servings sesuai dengan makanan yang diupdate"
    )

    number_of_units: float = Field(
        gt=0, 
        description="Jumlah unit baru yang dikonsumsi user"
    )

    meal_type: Optional[MealType] = Field(
        default=None,
        description= "Jenis makan baru (Breakfast, Lunch, Dinner, Snack). Isi hanya jika user ingin mengubah jenis makan. Jika tidak, biarkan kosong."
    )

class BulkUpdateFoodLogSchema(BaseModel):
    updates: List[BulkUpdateFoodLogItem] = Field(min_length=1)

class BulkAddFoodLogSchema(BaseModel):
    items: List[CreateFoodLogSchema] = Field(
        min_length=1,
        description="List makanan yang akan ditambahkan ke food log"
    )