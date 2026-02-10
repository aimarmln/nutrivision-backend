from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import MealLog, Food
from extensions import db
from utils.food import predict_food
from datetime import datetime, timezone

food_bp = Blueprint('food', __name__)

@food_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    if 'image' not in request.files:
        return jsonify({'msg': 'Image file is required'}), 400
    
    image = request.files['image']
    predictions = predict_food(image)

    results = []

    for pred in predictions:
        food_id = pred.get('class_id')
        food_item = Food.query.get(food_id)

        if not food_item:
            return jsonify({'msg': f'Food with id {food_id} not found'}), 404

        weight = food_item.instance_weight_g * pred.get('count')

        result = {
            'id': food_item.id, 
            'food_name': food_item.food_name,
            'weight': weight,
            'calories_kcal': round((food_item.calories_per_100g_kcal / 100) * weight),
            'carbohydrates_g': round((food_item.carbohydrate_per_100g_g / 100) * weight, 1),
            'proteins_g': round((food_item.protein_per_100g_g / 100) * weight, 1),
            'fats_g': round((food_item.fat_per_100g_g / 100) * weight, 1)
        }

        results.append(result)

    return jsonify(results), 200

@food_bp.route('/', methods=['GET'])
def all():
    foods = Food.query.all()
    return jsonify([{
        'id': food.id,
        'food_name': food.food_name,
        'weight': 100,
        'calories_kcal': round(food.calories_per_100g_kcal),
        'carbohydrates_g': round(food.carbohydrate_per_100g_g, 1),
        'proteins_g': round(food.protein_per_100g_g, 1),
        'fats_g': round(food.fat_per_100g_g, 1)
    } for food in foods]), 200

@food_bp.route('/log', methods=['POST'])
@jwt_required()
def log():
    data = request.get_json()

    if not data:
        return jsonify({'msg': 'Missing JSON in request'}), 400
    
    user_id = get_jwt_identity()

    food_id = data.get('food_id')
    weight = data.get('weight_grams')
    meal_type = data.get('meal_type')

    food = Food.query.get(food_id)
    if not food:
        return jsonify({'msg': f'Food with id {food_id} not found'}), 404

    calories = round((food.calories_per_100g_kcal / 100) * weight)
    carbohydrates = round((food.carbohydrate_per_100g_g / 100) * weight, 1)
    proteins = round((food.protein_per_100g_g / 100) * weight, 1)
    fats = round((food.fat_per_100g_g / 100) * weight, 1)

    new_log = MealLog(
        user_id=user_id,
        food_id=food_id,
        meal_type=meal_type,
        weight_grams=weight,
        calories=calories,
        carbohydrates=carbohydrates,
        proteins=proteins,
        fats=fats,
        logged_at=datetime.now(timezone.utc)
    )

    db.session.add(new_log)
    db.session.commit()

    return jsonify({'msg': f'Successfully logged: {food.food_name}'}), 201

@food_bp.route('/<int:food_id>', methods=['GET'])
def food_detail(food_id):
    food = Food.query.get(food_id)
    if not food:
        return jsonify({'msg': f'Food with id {food_id} not found'}), 404
    
    return jsonify({
        'food_name': food.food_name,
        'calories_per_100g_kcal': round(food.calories_per_100g_kcal),
        'carbohydrate_per_100g_g': round(food.carbohydrate_per_100g_g, 1),
        'protein_per_100g_g': round(food.protein_per_100g_g, 1),
        'fat_per_100g_g': round(food.fat_per_100g_g, 1),
    }), 200

@food_bp.route('/search', methods=['GET'])
def search_food():
    query = request.args.get('query', '').lower()
    results = Food.query.filter(Food.food_name.ilike(f'%{query}%')).all()

    return jsonify([{
        'id': food.id,
        'food_name': food.food_name,
        'weight': 100,
        'calories_kcal': round(food.calories_per_100g_kcal),
        'carbohydrates_g': round(food.carbohydrate_per_100g_g, 1),
        'proteins_g': round(food.protein_per_100g_g, 1),
        'fats_g': round(food.fat_per_100g_g, 1)
    } for food in results]), 200

@food_bp.route('/nutrition-calc', methods=['GET'])
def calculate_nutrition():
    food_id = request.args.get('food_id', type=int)
    weight = request.args.get('weight_grams', type=int)

    food = Food.query.get(food_id)
    if not food:
        return jsonify({'msg': f'Food with id {food_id} not found'}), 404

    return jsonify({
        'calories_kcal': round((food.calories_per_100g_kcal / 100) * weight),
        'carbohydrates_g': round((food.carbohydrate_per_100g_g / 100) * weight, 1),
        'proteins_g': round((food.protein_per_100g_g / 100) * weight, 1),
        'fats_g': round((food.fat_per_100g_g / 100) * weight, 1)
    }), 200
