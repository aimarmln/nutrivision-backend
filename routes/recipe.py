from flask import Blueprint, jsonify, request
from models import Recipe, Comment, User
from utils.recipe import get_ingredients_list, get_instructions_list

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
def all():
    recipes = Recipe.query.order_by(Recipe.id).all()
    result = []
    for recipe in recipes:
        positive_comment_count = Comment.query.filter_by(recipe_id=recipe.id, sentiment='Positive').count()
        result.append({
            'id': recipe.id,
            'recipe_name': recipe.recipe_name,
            'calories_per_serving_kcal': round(recipe.calories_per_serving_kcal),
            'carbohydrate_per_serving_g': round(recipe.carbohydrate_per_serving_g, 1),
            'protein_per_serving_g': round(recipe.protein_per_serving_g, 1),
            'fat_per_serving_g': round(recipe.fat_per_serving_g, 1),
            'health_category': recipe.health_category,
            'positive_comment_count': positive_comment_count
        })

    return jsonify(result), 200

@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe_detail(recipe_id):
    

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'msg': 'Recipe not found'}), 404

    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    positive_comment_count = sum(1 for comment in comments if comment.sentiment == 'Positive')

    enriched_comments = []
    for comment in comments:
        user = User.query.get(comment.user_id)
        enriched_comments.append({
            'id': comment.id,
            'name': user.name if user else 'Unknown User',
            'text': comment.text,
            'sentiment': comment.sentiment
        })

    return jsonify({
        'id': recipe.id,
        'recipe_name': recipe.recipe_name,
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
        'comments': enriched_comments
    }), 200

@recipe_bp.route('/search', methods=['GET'])
def search_recipe():
    query = request.args.get('query', '').strip()
    results = Recipe.query.filter(Recipe.recipe_name.ilike(f'%{query}%')).all()

    response = []
    for recipe in results:
        positive_comment_count = Comment.query.filter_by(recipe_id=recipe.id, sentiment='Positive').count()
        response.append({
            'id': recipe.id,
            'recipe_name': recipe.recipe_name,
            'calories_per_serving_kcal': round(recipe.calories_per_serving_kcal),
            'carbohydrate_per_serving_g': round(recipe.carbohydrate_per_serving_g, 1),
            'protein_per_serving_g': round(recipe.protein_per_serving_g, 1),
            'fat_per_serving_g': round(recipe.fat_per_serving_g, 1),
            'health_category': recipe.health_category,
            'positive_comment_count': positive_comment_count
        })

    return jsonify(response), 200
