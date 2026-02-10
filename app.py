from flask import Flask
from extensions import db, jwt
from routes.auth import auth_bp
from routes.user import user_bp
from routes.recipe import recipe_bp
from routes.comment import comment_bp
from routes.food import food_bp
from routes.meal_log import meal_log_bp
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load configuration from .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(recipe_bp, url_prefix='/recipe')
    app.register_blueprint(comment_bp, url_prefix='/comment')
    app.register_blueprint(food_bp, url_prefix='/food')
    app.register_blueprint(meal_log_bp, url_prefix='/meal-log')

    return app
