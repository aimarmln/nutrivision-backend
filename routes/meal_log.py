from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import MealLog, Food
from extensions import db
from datetime import datetime, timezone

meal_log_bp = Blueprint('meal-log', __name__)

@meal_log_bp.route('/<int:meal_id>', methods=['GET'])
@jwt_required()
def meal_detail(meal_id):
    meal = MealLog.query.get(meal_id)
    if not meal:
        return jsonify({'msg': 'Meal log not found'}), 404
    
    food = Food.query.get(meal.food_id)
    if not food:
        return jsonify({'msg': 'Associated food item not found'}), 404

    return jsonify({
        'id': meal.id,
        'food_name': food.food_name,
        'weight_grams': round(meal.weight_grams),
        'calories': round(meal.calories),
        'carbohydrates': meal.carbohydrates,
        'proteins': meal.proteins,
        'fats': meal.fats,
    }), 200

@meal_log_bp.route('/<int:meal_id>', methods=['PUT'])
@jwt_required()
def update_meal(meal_id):
    meal = MealLog.query.get(meal_id)
    if not meal:
        return jsonify({'msg': 'Meal log not found'}), 404
    
    food = Food.query.get(meal.food_id)
    if not food:
        return jsonify({'msg': 'Associated food item not found'}), 404

    data = request.get_json()
    new_weight = data.get('weight_grams', meal.weight_grams)

    new_calories = round((food.calories_per_100g_kcal / 100) * new_weight)
    new_carbohydrates = round((food.carbohydrate_per_100g_g / 100) * new_weight, 1)
    new_proteins = round((food.protein_per_100g_g / 100) * new_weight, 1)
    new_fats = round((food.fat_per_100g_g / 100) * new_weight, 1)

    meal.weight_grams = new_weight
    meal.calories = new_calories
    meal.carbohydrates = new_carbohydrates
    meal.proteins = new_proteins
    meal.fats = new_fats
    meal.logged_at = datetime.now(timezone.utc)

    db.session.commit()

    return jsonify({'msg': 'Meal log updated successfully',}), 200

@meal_log_bp.route('/<int:meal_id>', methods=['DELETE'])
@jwt_required()
def delete_meal(meal_id):
    meal = MealLog.query.get(meal_id)
    if not meal:
        return jsonify({'msg': 'Meal log not found'}), 404

    db.session.delete(meal)
    db.session.commit()

    return jsonify({'msg': f'Meal log deleted successfully'}), 200