from extensions import db
from datetime import datetime, timezone

class MealLog(db.Model):
    __tablename__ = 'meal_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)

    meal_type = db.Column(db.Enum(
        'Breakfast', 'Lunch', 'Dinner', 'Snacks',
        name='meal_type_enum'
    ), nullable=False)


    weight_grams = db.Column(db.Float, nullable=False) 
    calories = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    proteins = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)

    logged_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('meal_logs', lazy=True))
    food_item = db.relationship('Food', backref=db.backref('meal_logs', lazy=True))
