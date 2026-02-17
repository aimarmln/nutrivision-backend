from enum import Enum

class MealType(str, Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACK = "Snack"

    def __str__(self) -> str:
        return str(self.value)
