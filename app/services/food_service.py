import uuid
from werkzeug.exceptions import NotFound, InternalServerError
from werkzeug.datastructures import FileStorage
from app.schemas.food_schema import FoodsListQueryParams
from app.extensions import yolo_detector
from app.repositories.food_repository import FoodRepository

class FoodService:

    @staticmethod
    def get_all_foods(params: FoodsListQueryParams) -> tuple[list[dict], dict]:
        # Count total items for pagination
        total_items = FoodRepository.count_all(search_query=params.q)

        # Call repository to get all foods
        foods = FoodRepository.find_all_paginated(
            page=params.page, 
            limit=params.limit, 
            search_query=params.q, 
            preload_servings=True
        )

        # Build results with default serving information
        results = []
        for food in foods:
            # Find the default serving for the food
            default_serving = next((s for s in food.servings if s.is_default), None)
            if not default_serving:
                raise InternalServerError(f'Default serving not found for food: {food.name}')

            results.append({
                'id': food.id,
                'food_name': food.name,
                'serving': {
                    'id': default_serving.id,
                    'number_of_units': default_serving.number_of_units,
                    'serving_unit': default_serving.serving_unit,
                    'description': default_serving.description,
                    'calories_kcal': round(default_serving.calories_kcal),
                    'carbohydrates_g': round(default_serving.carbohydrate_g, 1),
                    'proteins_g': round(default_serving.protein_g, 1),
                    'fats_g': round(default_serving.fat_g, 1),
                    'is_default': default_serving.is_default,
                }
            })

        # Build pagination info
        total_pages = (total_items + params.limit - 1) // params.limit
        pagination = {
            'current_page': params.page,
            'limit': params.limit,
            'total_items': total_items,
            'total_pages': total_pages, 
        }

        return results, pagination

    @staticmethod
    def get_food_detail(food_id: uuid.UUID):
        # Retrieve food detail by ID
        food = FoodRepository.find_by_id(id=food_id, preload_servings=True)
        if not food:
            raise NotFound('Food not found')
        
        servings_sorted = sorted(
            food.servings,
            key=lambda s: not s.is_default
        )
        
        servings_list = [
            {
                'id': serving.id,
                'number_of_units': serving.number_of_units,
                'serving_unit': serving.serving_unit,
                'description': serving.description,
                'calories_kcal': round(serving.calories_kcal),
                'carbohydrates_g': round(serving.carbohydrate_g, 1),
                'proteins_g': round(serving.protein_g, 1),
                'fats_g': round(serving.fat_g, 1),
                'is_default': serving.is_default,
            }
            for serving in servings_sorted
        ]
        
        result = {
            'id': food.id,
            'food_name': food.name,
            'food_category': food.category,
            'food_subcategory': food.subcategory,
            'servings': servings_list,  
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
        labels = list({item.get('label') for item in detection_results})

        # Query foods by YOLO labels
        foods = FoodRepository.find_by_yolo_labels(labels, preload_servings=True)

        # Create a mapping of YOLO label to food item for easy lookup
        food_map = {food.yolo_label: food for food in foods}

        # Build results
        results = []
        for item in detection_results:
            label = item.get('label')
            count = item.get('count', 1)

            food_item = food_map.get(label) # Find the food item based on YOLO label
            if not food_item:
                raise InternalServerError(f'Food item not found for YOLO label: {label}')

            # Find the default serving for the food
            default_serving = next((s for s in food_item.servings if s.is_default), None)
            if not default_serving:
                raise InternalServerError(f'Default serving not found for food: {food_item.name}')

            # Calculate weight based on instance weight and detection count
            number_of_units = default_serving.number_of_units * count
            factor = number_of_units / default_serving.number_of_units

            calories_kcal = default_serving.calories_kcal * factor
            carbohydrates_g = default_serving.carbohydrate_g * factor
            proteins_g = default_serving.protein_g * factor
            fats_g = default_serving.fat_g * factor

            results.append({
                'id': str(food_item.id),
                'food_name': food_item.name,
                'serving': {
                    'id': default_serving.id,
                    'number_of_units': number_of_units,
                    'serving_unit': default_serving.serving_unit,
                    'description': default_serving.description,
                    'calories_kcal': round(calories_kcal),
                    'carbohydrates_g': round(carbohydrates_g, 1),
                    'proteins_g': round(proteins_g, 1),
                    'fats_g': round(fats_g, 1),
                    'is_default': default_serving.is_default,
                }
            })

        return results
