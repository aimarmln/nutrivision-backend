import uuid
from werkzeug.exceptions import NotFound, InternalServerError
from werkzeug.datastructures import FileStorage
from app.extensions import yolo_detector
from app.repositories.food_repository import FoodRepository

class FoodService:

    @staticmethod
    def get_all_foods(search_query: str | None = None):
        # Call repository to get all foods
        foods =  FoodRepository.find_all(search_query)

        results = [
            {
                'id': food.id,
                'food_name': food.name,
                'weight': 100,
                'calories_kcal': round(food.calories_per_100g_kcal),
                'carbohydrates_g': round(food.carbohydrate_per_100g_g, 1),
                'proteins_g': round(food.protein_per_100g_g, 1),
                'fats_g': round(food.fat_per_100g_g, 1)
            } 
            for food in foods
        ]

        return results

    @staticmethod
    def get_food_detail(food_id: uuid.UUID):
        # Retrieve food detail by ID
        food = FoodRepository.find_by_id(food_id)
        if not food:
            raise NotFound('Food not found')
        
        result = {
            'id': food.id,
            'food_name': food.name,
            'calories_per_100g_kcal': round(food.calories_per_100g_kcal),
            'carbohydrate_per_100g_g': round(food.carbohydrate_per_100g_g, 1),
            'protein_per_100g_g': round(food.protein_per_100g_g, 1),
            'fat_per_100g_g': round(food.fat_per_100g_g, 1),
        }

        return result
    
    @staticmethod
    def detect_foods(image: FileStorage):
        # Detect food with YOLO model
        detection_results = yolo_detector.detect(image)

        # If no detection results, return empty list
        if not detection_results:
            return []

        # Get unique labels from detection results
        labels = list({item.get("label") for item in detection_results})

        # Query foods by YOLO labels
        foods = FoodRepository.find_by_yolo_labels(labels)

        # Create a mapping of YOLO label to food item for easy lookup
        food_map = {food.yolo_label: food for food in foods}

        # Build results
        results = []
        for item in detection_results:
            label = item.get("label")
            count = item.get("count", 1)

            food_item = food_map.get(label) # Find the food item based on YOLO label

            if not food_item:
                raise InternalServerError(f"Food item not found for YOLO label: {label}")

            # Calculate weight based on instance weight and detection count
            weight = food_item.instance_weight_g * count

            results.append({
                "id": str(food_item.id),
                "food_name": food_item.name,
                "weight": weight,
                "calories_kcal": round((food_item.calories_per_100g_kcal / 100) * weight),
                "carbohydrates_g": round((food_item.carbohydrate_per_100g_g / 100) * weight, 1),
                "proteins_g": round((food_item.protein_per_100g_g / 100) * weight, 1),
                "fats_g": round((food_item.fat_per_100g_g / 100) * weight, 1),
            })

        return results
