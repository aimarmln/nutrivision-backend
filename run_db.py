from app import create_app
from extensions import db
from models import Recipe, Food
import pandas as pd

app = create_app()

with app.app_context():
    db.create_all()

    if Recipe.query.first() is None:
        df_recipe = pd.read_csv('datasets/recipes.csv')
        df_recipe = df_recipe.drop(columns=['detail_url'])
        for _, row in df_recipe.iterrows():
            rec = Recipe(**row.to_dict())
            db.session.add(rec)

    if Food.query.first() is None:
        df_food = pd.read_csv('datasets/foods.csv')
        df_food = df_food.drop(columns=['detail_url'])
        for _, row in df_food.iterrows():
            food = Food(**row.to_dict())
            db.session.add(food)

    db.session.commit()
    print("Database tables created and populated.")
