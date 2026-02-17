import uuid
from datetime import datetime, timezone
from werkzeug.exceptions import NotFound
from app.repositories.food_repository import FoodRepository
from app.repositories.food_log_repository import FoodLogRepository
from app.models.food_log import FoodLog
from app.schemas.food_log_schema import CreateFoodLogSchema, UpdateFoodLogSchema

class FoodLogService:
    
    @staticmethod
    def create_food_log(user_id: uuid.UUID, data: CreateFoodLogSchema):
        # Validate food exists
        food = FoodRepository.find_by_id(data.food_id)
        if not food:
            raise NotFound('Food not found')
        
        # Get factor for nutritional calculation
        factor = data.weight_grams / 100

        # Calculate nutritional values
        calories = food.calories_per_100g_kcal * factor
        carbs = food.carbohydrate_per_100g_g * factor
        proteins = food.protein_per_100g_g * factor
        fats = food.fat_per_100g_g * factor

        # Create food log entry
        food_log = FoodLog(
            id=uuid.uuid4(),
            user_id=user_id,
            food_id=data.food_id,
            meal_type=data.meal_type,
            weight_grams=data.weight_grams,
            calories=calories,
            carbohydrates=carbs,
            proteins=proteins,
            fats=fats
        )

        # Save food log to database     
        saved_log = FoodLogRepository.save(food_log)

        return {
            'id': saved_log.id,
            'food_name': food.name,
            'weight_grams': round(saved_log.weight_grams),
            'calories': round(saved_log.calories),
            'carbohydrates': saved_log.carbohydrates,
            'proteins': saved_log.proteins,
            'fats': saved_log.fats,
        }
    
    @staticmethod
    def get_food_log_detail(user_id: uuid.UUID, food_log_id: uuid.UUID):
        # Retrieve food log entry
        food_log = FoodLogRepository.find_by_id_and_user(food_log_id, user_id, preload_food=True)
        if not food_log:
            raise NotFound('Food log not found')
        
        return {
            'id': food_log.id,
            'food_name': food_log.food.name,
            'weight_grams': round(food_log.weight_grams),
            'calories': round(food_log.calories),
            'carbohydrates': food_log.carbohydrates,
            'proteins': food_log.proteins,
            'fats': food_log.fats,
        }
    
    @staticmethod
    def update_food_log(user_id: uuid.UUID, food_log_id: uuid.UUID, data: UpdateFoodLogSchema):
        # Retrieve food log entry
        food_log = FoodLogRepository.find_by_id_and_user(food_log_id, user_id, preload_food=True)
        if not food_log:
            raise NotFound('Food log not found')
        
        # Calculate factor for nutritional values
        factor = data.weight_grams / 100
        food = food_log.food

        # Recalculate nutritional values
        food_log.weight_grams = data.weight_grams
        food_log.calories = food.calories_per_100g_kcal * factor
        food_log.carbohydrates = food.carbohydrate_per_100g_g * factor
        food_log.proteins = food.protein_per_100g_g * factor
        food_log.fats = food.fat_per_100g_g * factor
        food_log.updated_at = datetime.now(timezone.utc)    

        # Save updated food log
        FoodLogRepository.save(food_log)
        
        return
    
    @staticmethod
    def delete_food_log(user_id: uuid.UUID, food_log_id: uuid.UUID):
        # Retrieve food log entry
        food_log = FoodLogRepository.find_by_id_and_user(food_log_id, user_id)
        if not food_log:
            raise NotFound('Food log not found')
        
        # Soft delete food
        food_log.is_deleted = True
        food_log.deleted_at = datetime.now(timezone.utc)

        # Save changes
        FoodLogRepository.save(food_log)

        return
    