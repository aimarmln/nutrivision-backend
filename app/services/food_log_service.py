from typing import Optional
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from werkzeug.exceptions import NotFound, BadRequest
from app.constants.food_log import MealType
from app.repositories import FoodRepository, ServingRepository, FoodLogRepository
from app.models import FoodLog
from app.schemas.food_log_schema import (
    BulkAddFoodLogItem,
    BulkUpdateFoodLogItem,
    CreateFoodLogSchema,
    UpdateFoodLogSchema,
)
from app.utils.database import db_commit
from app.utils.food_log import resolve_meal_type


class FoodLogService:

    @staticmethod
    def create_food_log(user_id: int, data: CreateFoodLogSchema):
        # Validate food exists
        food = FoodRepository.find_by_id(data.food_id)
        if not food:
            raise NotFound("Food not found")

        # Validate serving exists
        serving = ServingRepository.find_by_id(data.serving_id)
        if not serving:
            raise NotFound("Serving not found")

        # Validate serving belongs to the specified food
        if serving.food_id != data.food_id:
            raise BadRequest("Serving does not belong to the specified food")

        # Create food log entry
        food_log = FoodLog(
            user_id=user_id,
            food_id=data.food_id,
            serving_id=data.serving_id,
            number_of_units=data.number_of_units,
            meal_type=data.meal_type,
        )

        # Save food log to database
        FoodLogRepository.save(food_log)
        db_commit()

        return

    @staticmethod
    def get_food_log_detail(user_id: int, food_log_id: int):
        # Retrieve food log entry
        food_log = FoodLogRepository.find_by_id_and_user(
            food_log_id,
            user_id,
            preload_food=True,
            preload_serving=True,
            preload_food_servings=True,
        )
        if not food_log:
            raise NotFound("Food log not found")

        # Calculate nutritional values based on serving and number of units
        serving = food_log.serving
        factor = food_log.number_of_units / food_log.serving.number_of_units

        total_calories = serving.calories_kcal * factor
        total_protein = serving.protein_g * factor
        total_fat = serving.fat_g * factor
        total_carbs = serving.carbohydrate_g * factor

        servings_sorted = sorted(food_log.food.servings, key=lambda s: not s.is_default)

        # Get all servings for this food
        servings_list = [
            {
                "id": serving.id,
                "number_of_units": serving.number_of_units,
                "serving_unit": serving.serving_unit,
                "description": serving.description,
                "calories_kcal": round(serving.calories_kcal),
                "carbohydrates_g": round(serving.carbohydrate_g, 1),
                "proteins_g": round(serving.protein_g, 1),
                "fats_g": round(serving.fat_g, 1),
                "is_default": serving.is_default,
            }
            for serving in servings_sorted
        ]

        return {
            "id": food_log.id,
            "food_name": food_log.food.name,
            "calories": round(total_calories),
            "carbohydrates": round(total_carbs, 2),
            "proteins": round(total_protein, 2),
            "fats": round(total_fat, 2),
            "meal_type": food_log.meal_type,
            "serving_id": food_log.serving_id,
            "number_of_units": food_log.number_of_units,
            "servings": servings_list,
        }

    @staticmethod
    def update_food_log(user_id: int, food_log_id: int, data: UpdateFoodLogSchema):
        # Retrieve food log entry
        food_log = FoodLogRepository.find_by_id_and_user(food_log_id, user_id)
        if not food_log:
            raise NotFound("Food log not found")

        # Validate serving exists
        serving = ServingRepository.find_by_id(data.serving_id)
        if not serving:
            raise NotFound("Serving not found")

        # Validate serving belongs to the specified food
        if serving.food_id != food_log.food_id:
            raise BadRequest("Serving does not belong to the specified food")

        # Update food log entry
        food_log.serving_id = data.serving_id
        food_log.number_of_units = data.number_of_units
        food_log.updated_at = datetime.now(timezone.utc)

        # Save updated food log
        FoodLogRepository.save(food_log)
        db_commit()

        return

    @staticmethod
    def delete_food_log(user_id: int, food_log_id: int):
        # Retrieve food log entry
        food_log = FoodLogRepository.find_by_id_and_user(food_log_id, user_id)
        if not food_log:
            raise NotFound("Food log not found")

        # Soft delete food
        food_log.is_deleted = True
        food_log.deleted_at = datetime.now(timezone.utc)

        # Save changes
        FoodLogRepository.save(food_log)
        db_commit()

        return food_log

    # AI utilities
    @staticmethod
    def get_today_logs(
        user_id: int, meal_types: Optional[list[MealType]] = None
    ) -> list[FoodLog]:
        logs = FoodLogRepository.find_by_user_id_and_date(
            user_id=user_id,
            log_date=datetime.now().date(),
            meal_types=meal_types,
            preload_food=True,
            preload_serving=True,
        )

        return logs

    @staticmethod
    def bulk_add_food_logs(
        user_id: int, logs: list[BulkAddFoodLogItem]
    ) -> list[FoodLog]:
        if not logs:
            raise BadRequest("No data provided")

        # Collect unique IDs
        food_ids = list(set(item.food_id for item in logs))
        serving_ids = list(set(item.serving_id for item in logs))

        # Fetch in batch
        foods = FoodRepository.find_many_by_ids(food_ids)
        servings = ServingRepository.find_many_by_ids(serving_ids)

        if len(foods) != len(food_ids):
            raise NotFound("Some foods not found")

        if len(servings) != len(serving_ids):
            raise NotFound("Some servings not found")

        serving_map = {s.id: s for s in servings}

        # now = datetime.now(timezone.utc)
        now = datetime.now(ZoneInfo("Asia/Jakarta")).replace(tzinfo=None)

        food_logs: list[FoodLog] = []

        for item in logs:
            serving = serving_map[item.serving_id]

            # Validate serving belongs to food
            if serving.food_id != item.food_id:
                raise BadRequest("Serving does not belong to the specified food")

            resolved_meal_type = resolve_meal_type(item.meal_type)

            food_log = FoodLog(
                user_id=user_id,
                food_id=item.food_id,
                serving_id=item.serving_id,
                number_of_units=item.number_of_units,
                meal_type=resolved_meal_type,
                created_at=now,
                updated_at=now,
            )

            food_logs.append(food_log)

        # Bulk insert
        FoodLogRepository.bulk_insert(food_logs)
        db_commit()

        log_ids = [log.id for log in food_logs]

        new_logs = FoodLogRepository.find_many_by_ids_and_user(
            log_ids, user_id, preload_food=True, preload_serving=True
        )

        return new_logs

    @staticmethod
    def bulk_edit_food_logs(
        user_id: int, updates: list[BulkUpdateFoodLogItem]
    ) -> list[FoodLog]:
        # Get all log IDs from the updates
        log_ids = [item.id for item in updates]

        # Get all logs in a single query
        logs = FoodLogRepository.find_many_by_ids_and_user(
            log_ids, user_id, preload_food=True, preload_serving=True
        )

        if len(logs) != len(log_ids):
            raise NotFound("Some food logs not found")

        logs_map = {log.id: log for log in logs}

        # Get all unique serving IDs from the updates
        serving_ids = list(set(item.serving_id for item in updates))

        servings = ServingRepository.find_many_by_ids(serving_ids, preload_food=True)
        serving_map = {s.id: s for s in servings}

        if len(servings) != len(serving_ids):
            raise NotFound("Some servings not found")

        now = datetime.now(timezone.utc)

        updated_logs = []

        for item in updates:
            log = logs_map[item.id]
            serving = serving_map[item.serving_id]

            is_replace = item.food_id is not None

            if is_replace:
                if serving.food_id != item.food_id:
                    raise BadRequest("Serving does not belong to the new food")
            else:
                if serving.food_id != log.food_id:
                    raise BadRequest(
                        "Serving does not belong to the same food as the log"
                    )

            # Update
            if is_replace:
                log.food_id = item.food_id
                log.food = serving.food

            if item.meal_type is not None:
                log.meal_type = item.meal_type

            log.serving_id = item.serving_id
            log.serving = serving
            log.number_of_units = item.number_of_units
            log.updated_at = now

            updated_logs.append(log)

        # Bulk update logs in a single transaction
        FoodLogRepository.bulk_update(updated_logs)
        db_commit()

        return updated_logs

    @staticmethod
    def bulk_delete_food_logs(user_id: int, log_ids: list[int]) -> list[FoodLog]:
        if not log_ids:
            raise BadRequest("No log IDs provided")

        # Get all logs in a single query
        logs = FoodLogRepository.find_many_by_ids_and_user(
            log_ids, user_id, preload_food=True, preload_serving=True
        )

        if len(logs) != len(log_ids):
            raise NotFound("Some food logs not found or not owned by user")

        now = datetime.now(timezone.utc)

        # Soft delete all logs
        for log in logs:
            log.is_deleted = True
            log.deleted_at = now

        # Bulk delete logs in a single transaction
        FoodLogRepository.bulk_update(logs)
        db_commit()

        return logs
