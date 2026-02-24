import uuid
from datetime import datetime, timezone
from werkzeug.exceptions import NotFound, BadRequest
from app.repositories.food_repository import FoodRepository
from app.repositories.serving_repository import ServingRepository
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
        
        # Validate serving exists
        serving = ServingRepository.find_by_id(data.serving_id)
        if not serving:
            raise NotFound('Serving not found')
        
        # Validate serving belongs to the specified food
        if serving.food_id != data.food_id:
            raise BadRequest('Serving does not belong to the specified food')
        
        # Create food log entry
        food_log = FoodLog(
            id=uuid.uuid4(),
            user_id=user_id,
            food_id=data.food_id,
            serving_id=data.serving_id,
            number_of_units=data.number_of_units,
            meal_type=data.meal_type,
        )

        # Save food log to database     
        FoodLogRepository.save(food_log)

        return
    
    @staticmethod
    def get_food_log_detail(user_id: uuid.UUID, food_log_id: uuid.UUID):
        # Retrieve food log entry
        food_log = FoodLogRepository.find_by_id_and_user(
            food_log_id, 
            user_id, 
            preload_food=True, 
            preload_serving=True,
            preload_food_servings=True
        )
        if not food_log:
            raise NotFound('Food log not found')
        
        # Calculate nutritional values based on serving and number of units
        serving = food_log.serving
        factor = food_log.number_of_units / food_log.serving.number_of_units

        total_calories = serving.calories_kcal * factor
        total_protein = serving.protein_g * factor
        total_fat = serving.fat_g * factor
        total_carbs = serving.carbohydrate_g * factor

        # Get all servings for this food
        servings_list = [
            {
                'id': serving.id,
                'number_of_units': serving.number_of_units,
                'serving_unit': serving.serving_unit,
                'description': serving.description,
                'calories_kcal': round(serving.calories_kcal),
                'carbohydrates_g': round(serving.carbohydrate_g, 1),
                'proteins_g': round(serving.protein_g, 1),
                'fats_g': round(serving.fat_g, 1)
            }
            for serving in food_log.food.servings
        ]
        
        return {
            'id': food_log.id,
            'food_name': food_log.food.name,
            'calories': round(total_calories),
            'carbohydrates': round(total_carbs, 2),
            'proteins': round(total_protein, 2),
            'fats': round(total_fat, 2),
            'meal_type': food_log.meal_type,
            'serving_id': food_log.serving_id,
            'number_of_units': factor,
            'servings': servings_list,
        }
    
    @staticmethod
    def update_food_log(user_id: uuid.UUID, food_log_id: uuid.UUID, data: UpdateFoodLogSchema):
        # Retrieve food log entry
        food_log = FoodLogRepository.find_by_id_and_user(food_log_id, user_id)
        if not food_log:
            raise NotFound('Food log not found')
        
        # Validate serving exists
        serving = ServingRepository.find_by_id(data.serving_id)
        if not serving:
            raise NotFound('Serving not found')
        
        # Validate serving belongs to the specified food
        if serving.food_id != food_log.food_id:
            raise BadRequest('Serving does not belong to the specified food')

        # Update food log entry
        food_log.serving_id = data.serving_id
        food_log.number_of_units = data.number_of_units
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
    