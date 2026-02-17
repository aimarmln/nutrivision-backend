import uuid
from werkzeug.exceptions import NotFound
from app.repositories.recipe_repository import RecipeRepository
from app.repositories.comment_repository import CommentRepository
from app.utils.recipe import get_ingredients_list, get_instructions_list
from app.models.recipe import Recipe
from app.models.user import User

class RecipeService:
    
    @staticmethod
    def get_all_recipes(search_query: str = None):
        # Retrieve all recipes with their positive comment counts
        recipes = RecipeRepository.find_all_with_positive_comment_count(search_query)

        return [
            {
                'id': recipe.id,
                'recipe_name': recipe.name,
                'calories_per_serving_kcal': round(recipe.calories_per_serving_kcal),
                'carbohydrate_per_serving_g': round(recipe.carbohydrate_per_serving_g, 1),
                'protein_per_serving_g': round(recipe.protein_per_serving_g, 1),
                'fat_per_serving_g': round(recipe.fat_per_serving_g, 1),
                'health_category': recipe.health_category,
                'positive_comment_count': positive_comment_count
            }
            for recipe, positive_comment_count in recipes
        ]
    
    @staticmethod
    def get_recipe_detail(recipe_id: uuid.UUID):
        # Retrieve recipe detail by ID
        recipe = RecipeRepository.find_by_id(recipe_id)
        if not recipe:
            raise NotFound('Recipe not found')
        
        # Retrieve comments
        comments = CommentRepository.find_by_recipe_id(recipe_id)
        positive_comment_count = sum(1 for comment in comments if comment.sentiment == 'Positive')

        return {
            'id': recipe.id,
            'recipe_name': recipe.name,
            'description': recipe.description,
            'ingredients': get_ingredients_list(recipe.ingredients),
            'instructions': get_instructions_list(recipe.instructions),
            'serving_yield': recipe.serving_yield,
            'calories_per_serving_kcal': round(recipe.calories_per_serving_kcal),
            'fat_per_serving_g': round(recipe.fat_per_serving_g, 1),
            'protein_per_serving_g': round(recipe.protein_per_serving_g, 1),
            'carbohydrate_per_serving_g': round(recipe.carbohydrate_per_serving_g, 1),
            'health_category': recipe.health_category,
            'positive_comment_count': positive_comment_count,
            'comments': [
                {
                    'id': comment.id,
                    'name': comment.user.name,
                    'text': comment.text,
                    'sentiment': comment.sentiment,
                }
                for comment in comments
            ],
        }
    
        