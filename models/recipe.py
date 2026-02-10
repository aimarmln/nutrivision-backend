from extensions import db

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)

    recipe_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    serving_yield = db.Column(db.Integer, nullable=False)
    
    calories_per_serving_kcal = db.Column(db.Float, nullable=False)
    fat_per_serving_g = db.Column(db.Float, nullable=False)
    cholesterol_per_serving_mg = db.Column(db.Float, nullable=False)
    protein_per_serving_g = db.Column(db.Float, nullable=False)
    carbohydrate_per_serving_g = db.Column(db.Float, nullable=False)
    fiber_per_serving_g = db.Column(db.Float, nullable=False)
    sugar_per_serving_g = db.Column(db.Float, nullable=False)
    sodium_per_serving_mg = db.Column(db.Float, nullable=False)
    kalium_per_serving_mg = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255))
    health_category = db.Column(db.Enum(
        'Healthy', 'Unhealthy',
        name='health_category_enum'
    ), nullable=False)
