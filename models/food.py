from extensions import db

class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    
    food_name = db.Column(db.String(100), nullable=False)
    calories_per_100g_kcal = db.Column(db.Float, nullable=False)
    fat_per_100g_g = db.Column(db.Float, nullable=False)
    cholesterol_per_100g_mg = db.Column(db.Float, nullable=False)
    protein_per_100g_g = db.Column(db.Float, nullable=False)
    carbohydrate_per_100g_g = db.Column(db.Float, nullable=False)
    fiber_per_100g_g = db.Column(db.Float, nullable=False)
    sugar_per_100g_g = db.Column(db.Float, nullable=False)
    sodium_per_100g_mg = db.Column(db.Float, nullable=False)
    kalium_per_100g_mg = db.Column(db.Float, nullable=False)
    instance_weight_g = db.Column(db.Integer, nullable=True)