from werkzeug.exceptions import NotFound
from app.repositories import RecipeRepository, CommentRepository
from app.schemas.recipe_schema import RecipesListQueryParams
from app.utils.recipe import get_ingredients_list, get_instructions_list


class RecipeService:
    
    @staticmethod
    def get_all_recipes(params: RecipesListQueryParams) -> tuple[list[dict], dict]:
        # Count total items for pagination
        total_items = RecipeRepository.count_all(search_query=params.q)

        # Retrieve all recipes with their positive comment counts
        recipes = RecipeRepository.find_all_paginated(
            search_query=params.q, 
            page=params.page, 
            limit=params.limit, 
            include_positive_comment_count=True
        )

        results = [
            {
                'id': recipe.id,
                'image_path': recipe.image_path,
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
    def get_recipe_detail(recipe_id: int):
        # Retrieve recipe detail by ID
        recipe = RecipeRepository.find_by_id(recipe_id)
        if not recipe:
            raise NotFound('Recipe not found')
        
        # Retrieve comments
        positive_comment_count = CommentRepository.count_positive_comments_by_recipe_id(recipe_id)

        return {
            'id': recipe.id,
            'image_path': recipe.image_path,
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
        }
        