from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, MealLog
from extensions import db
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from utils.user import regenerate_user_metrics

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    today = datetime.now(ZoneInfo('Asia/Jakarta')).date()

    logs = MealLog.query.filter_by(user_id=user_id).all()
    today_logs = [log for log in logs if log.logged_at.date() == today]

    grouped_logs = defaultdict(list)
    calories_per_meal = defaultdict(float)

    total_calories = 0
    total_carbs = 0
    total_proteins = 0
    total_fats = 0

    for log in today_logs:
        grouped_logs[log.meal_type].append({
            'meal_id': log.id,
            'food_id': log.food_item.id,
            'food_name': log.food_item.food_name,
            'calories': round(log.calories),
        })

        total_calories += log.calories
        total_carbs += log.carbohydrates
        total_proteins += log.proteins
        total_fats += log.fats

        calories_per_meal[log.meal_type] += log.calories

    return jsonify({
        'user': {
            'name': user.name,
            'calories_per_day': user.calories_per_day_kcal,
            'carbohydrates_per_day': user.carbohydrates_per_day_g,
            'calories_left': user.calories_per_day_kcal - round(total_calories),
            'proteins_per_day': user.proteins_per_day_g,
            'fats_per_day': user.fats_per_day_g,
            'calories_eaten': round(total_calories),
            'carbohydrates_eaten': round(total_carbs, 1),
            'proteins_eaten': round(total_proteins, 1),
            'fats_eaten': round(total_fats, 1),
        },
        'meal_logs': {
            'Breakfast': {
                'meals': grouped_logs.get('Breakfast', []),
                'total_calories': round(calories_per_meal.get('Breakfast', 0))
            },
            'Lunch': {
                'meals': grouped_logs.get('Lunch', []),
                'total_calories': round(calories_per_meal.get('Lunch', 0))
            },
            'Dinner': {
                'meals': grouped_logs.get('Dinner', []),
                'total_calories': round(calories_per_meal.get('Dinner', 0))
            },
            'Snacks': {
                'meals': grouped_logs.get('Snacks', []),
                'total_calories': round(calories_per_meal.get('Snacks', 0))
            }
        }
    }), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    return jsonify({
        'id': user.id,
        'name': user.name,
        'birthday': user.birthday.isoformat(),
        'age': user.age,
        'height_cm': user.height_cm,
        'weight_kg': user.weight_kg,
        'activity_level': user.activity_level,
        'main_goal': user.main_goal,
        'bmi': user.bmi,
        'bmi_status': user.bmi_status,
    }), 200

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    data = request.get_json()
    combined_data = {
        'email': data.get('email', user.email),
        'name': data.get('name', user.name),
        'gender': data.get('gender', user.gender),
        'birthday': str(user.birthday) if not data.get('birthday') else data.get('birthday'),
        'height_cm': data.get('height_cm', user.height_cm),
        'weight_kg': data.get('weight_kg', user.weight_kg),
        'activity_level': data.get('activity_level', user.activity_level),
        'main_goal': data.get('main_goal', user.main_goal),
    }

    updated_data = regenerate_user_metrics(combined_data)

    user.email = updated_data['email']
    user.name = updated_data['name']
    user.gender = updated_data['gender']
    user.birthday = updated_data['birthday']
    user.age = updated_data['age']
    user.height_cm = updated_data['height_cm']
    user.weight_kg = updated_data['weight_kg']
    user.activity_level = updated_data['activity_level']
    user.main_goal = updated_data['main_goal']
    user.bmr = updated_data['bmr']
    user.bmi = updated_data['bmi']
    user.bmi_status = updated_data['bmi_status']
    user.calories_per_day_kcal = updated_data['calories_per_day_kcal']
    user.carbohydrates_per_day_g = updated_data['carbohydrates_per_day_g']
    user.proteins_per_day_g = updated_data['proteins_per_day_g']
    user.fats_per_day_g = updated_data['fats_per_day_g']

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200
