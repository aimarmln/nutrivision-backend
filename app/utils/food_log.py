from datetime import datetime
from app.constants.food_log import MealType

def resolve_meal_type(meal_type: MealType | None) -> MealType:
    if meal_type:
        return meal_type

    hour = datetime.now().hour

    print(f"DEBUG MEAL_TYPE: RESOLVE FUNCTION - Current hour: {hour}")  # Debug statement

    if 5 <= hour < 11:
        return MealType.BREAKFAST
    elif 11 <= hour < 17:
        return MealType.LUNCH
    else:
        return MealType.DINNER