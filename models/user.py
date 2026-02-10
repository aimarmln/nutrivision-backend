from extensions import db
from datetime import datetime, timezone
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female', name='gender_enum'), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    height_cm = db.Column(db.Integer, nullable=False)
    weight_kg = db.Column(db.Integer, nullable=False)

    activity_level = db.Column(db.Enum(
        'Sedentary', 
        'Lightly Active', 
        'Moderately Active', 
        'Active', 
        'Very Active', 
        name='activity_level_enum'
    ), nullable=False)

    main_goal = db.Column(db.Enum(
        'Lose Weight', 
        'Maintain Weight', 
        'Gain Weight', 
        name='main_goal_enum'
    ), nullable=False)

    bmr = db.Column(db.Float, nullable=False)

    bmi = db.Column(db.Float, nullable=False)
    bmi_status = db.Column(db.Enum(
        'Underweight',
        'Healthy',
        'Overweight',
        'Obesity Class I',
        'Obesity Class II',
        name='bmi_status_enum'
    ), nullable=False)
    
    calories_per_day_kcal = db.Column(db.Integer, nullable=False)
    carbohydrates_per_day_g = db.Column(db.Float, nullable=False)
    proteins_per_day_g = db.Column(db.Float, nullable=False)
    fats_per_day_g = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=func.now())
