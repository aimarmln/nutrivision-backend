from zoneinfo import ZoneInfo

from werkzeug.exceptions import NotFound, InternalServerError
from collections import defaultdict
from datetime import datetime, timezone
from app.repositories import UserRepository, FoodLogRepository
from app.models import User
from app.constants.food_log import MealType
from app.schemas.user_schema import CompleteUserProfileSchema, UpdateUserProfileSchema
from app.utils.database import db_commit
from app.utils.user import (
    calculate_age,
    calculate_bmi,
    determine_bmi_status,
    calculate_bmr,
    calculate_calories_per_day,
    calculate_macronutrients,
)


class UserService:

    @staticmethod
    def get_user_summary(user_id: int):
        # Retrieve user
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFound("User not found")

        # Retrieve today's food logs
        food_logs = FoodLogRepository.find_by_user_id_and_date(
            user_id=user_id,
            log_date=datetime.now(ZoneInfo("Asia/Jakarta")).date(),
            preload_food=True,
            preload_serving=True,
        )

        # Process and aggregate data
        grouped_logs = defaultdict(list)
        calories_per_meal = defaultdict(float)

        total_calories = 0
        total_carbs = 0
        total_proteins = 0
        total_fats = 0

        # Group food logs by meal type and calculate totals
        for log in food_logs:
            serving = log.serving
            factor = log.number_of_units / serving.number_of_units

            calories = serving.calories_kcal * factor
            proteins = serving.protein_g * factor
            fats = serving.fat_g * factor
            carbs = serving.carbohydrate_g * factor

            grouped_logs[log.meal_type].append(
                {
                    "food_log_id": log.id,
                    "food_id": log.food_id,
                    "food_name": log.food.name,
                    "calories": round(calories),
                    "created_at": log.created_at,
                }
            )

            total_calories += calories
            total_carbs += carbs
            total_proteins += proteins
            total_fats += fats

            calories_per_meal[log.meal_type] += calories

        return {
            "user_summary": {
                "name": user.name,
                "calories_per_day": user.calories_per_day_kcal,
                "calories_eaten": round(total_calories),
                "calories_left": user.calories_per_day_kcal - round(total_calories),
                "carbohydrates_per_day": user.carbohydrates_per_day_g,
                "carbohydrates_eaten": round(total_carbs, 1),
                "proteins_per_day": user.proteins_per_day_g,
                "proteins_eaten": round(total_proteins, 1),
                "fats_per_day": user.fats_per_day_g,
                "fats_eaten": round(total_fats, 1),
            },
            "food_logs": {
                MealType.BREAKFAST: {
                    "foods": sorted(
                        grouped_logs.get(MealType.BREAKFAST, []),
                        key=lambda x: x["created_at"],
                    ),
                    "total_calories": round(
                        calories_per_meal.get(MealType.BREAKFAST, 0)
                    ),
                },
                MealType.LUNCH: {
                    "foods": sorted(
                        grouped_logs.get(MealType.LUNCH, []),
                        key=lambda x: x["created_at"],
                    ),
                    "total_calories": round(calories_per_meal.get(MealType.LUNCH, 0)),
                },
                MealType.DINNER: {
                    "foods": sorted(
                        grouped_logs.get(MealType.DINNER, []),
                        key=lambda x: x["created_at"],
                    ),
                    "total_calories": round(calories_per_meal.get(MealType.DINNER, 0)),
                },
                MealType.SNACK: {
                    "foods": sorted(
                        grouped_logs.get(MealType.SNACK, []),
                        key=lambda x: x["created_at"],
                    ),
                    "total_calories": round(calories_per_meal.get(MealType.SNACK, 0)),
                },
            },
        }

    @staticmethod
    def get_user_profile(user_id: int):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFound("User not found")

        return {
            "id": user.id,
            "name": user.name,
            "birthday": user.birthday.isoformat(),
            "age": user.age,
            "height_cm": user.height_cm,
            "weight_kg": user.weight_kg,
            "activity_level": user.activity_level,
            "main_goal": user.main_goal,
            "bmi": user.bmi,
            "bmi_status": user.bmi_status,
        }

    @staticmethod
    def complete_user_profile(user_id: int, data: CompleteUserProfileSchema):
        # Retrieve user
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFound("User not found")

        # Update user with provided data
        user.name = data.name
        user.gender = data.gender
        birthday_date, age = calculate_age(data.birthday)
        user.birthday = birthday_date
        user.age = age
        user.height_cm = data.height_cm
        user.weight_kg = data.weight_kg
        user.activity_level = data.activity_level
        user.main_goal = data.main_goal
        user.updated_at = datetime.now(timezone.utc)

        # Recalculate metrics
        UserService.calculate_user_metrics(user)

        # Save updated user to database
        UserRepository.save(user)
        db_commit()

        return user

    @staticmethod
    def update_user_profile(user_id: int, data: UpdateUserProfileSchema):
        # Retrieve user
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise NotFound("User not found")

        # recalc flag
        recalc_required = False

        if data.name is not None:
            user.name = data.name

        # Fields affecting calculations
        # if data.gender is not None:
        #     user.gender = data.gender
        #     recalc_required = True

        if data.birthday is not None:
            birthday_date, age = calculate_age(data.birthday)
            user.birthday = birthday_date
            user.age = age
            recalc_required = True

        if data.height_cm is not None:
            user.height_cm = data.height_cm
            recalc_required = True

        if data.weight_kg is not None:
            user.weight_kg = data.weight_kg
            recalc_required = True

        if data.activity_level is not None:
            user.activity_level = data.activity_level
            recalc_required = True

        if data.main_goal is not None:
            user.main_goal = data.main_goal
            recalc_required = True

        # Recalculate metrics if needed
        if recalc_required:
            UserService.calculate_user_metrics(user)

        user.updated_at = datetime.now(timezone.utc)

        UserRepository.save(user)
        db_commit()

        return {
            "id": user.id,
            "name": user.name,
            "birthday": user.birthday.isoformat(),
            "age": user.age,
            "height_cm": user.height_cm,
            "weight_kg": user.weight_kg,
            "activity_level": user.activity_level,
            "main_goal": user.main_goal,
            "bmi": user.bmi,
            "bmi_status": user.bmi_status,
        }

    @staticmethod
    def calculate_user_metrics(user: User):
        # Make sure all required fields for calculations are present
        if not all([user.gender, user.height_cm, user.weight_kg, user.age]):
            raise InternalServerError("Missing required fields for calculations")

        bmi = calculate_bmi(user.height_cm, user.weight_kg)
        bmi_status = determine_bmi_status(bmi)
        bmr = calculate_bmr(user.gender, user.height_cm, user.weight_kg, user.age)
        calories_per_day = calculate_calories_per_day(
            bmr, user.activity_level, user.main_goal
        )
        macros = calculate_macronutrients(calories_per_day)

        user.bmi = bmi
        user.bmi_status = bmi_status
        user.bmr = bmr
        user.calories_per_day_kcal = calories_per_day
        user.carbohydrates_per_day_g = macros.get("carbohydrates", 0)
        user.proteins_per_day_g = macros.get("proteins", 0)
        user.fats_per_day_g = macros.get("fats", 0)
