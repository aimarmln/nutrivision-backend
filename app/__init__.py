from flask import Flask
from werkzeug.exceptions import (
    NotFound, 
    Forbidden, 
    Conflict, 
    Unauthorized,
    BadRequest,
    InternalServerError
)
from pydantic import ValidationError

from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.food_routes import food_bp
from app.routes.food_logs_routes import food_log_bp
from app.routes.recipe_routes import recipe_bp

from app.config import Config
from app.extensions import jwt

from app.utils.errors import (
    handle_expired_token,
    handle_invalid_token,
    handle_missing_token,
    handle_bad_request,
    handle_validation_error,
    handle_not_found,
    handle_forbidden,
    handle_internal_error,
    handle_conflict,
    handle_unauthorized
)

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    app.json.sort_keys = False  # Preserve order of keys in JSON responses

    # Initialize extensions
    jwt.init_app(app)

    jwt.expired_token_loader(handle_expired_token)
    jwt.invalid_token_loader(handle_invalid_token)
    jwt.unauthorized_loader(handle_missing_token)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(food_log_bp)
    app.register_blueprint(recipe_bp)

    # Register error handlers
    app.errorhandler(ValidationError)(handle_validation_error)
    app.errorhandler(BadRequest)(handle_bad_request)
    app.errorhandler(NotFound)(handle_not_found)
    app.errorhandler(Forbidden)(handle_forbidden)
    app.errorhandler(Conflict)(handle_conflict)
    app.errorhandler(Unauthorized)(handle_unauthorized)
    app.errorhandler(InternalServerError)(handle_internal_error)
    app.errorhandler(Exception)(handle_internal_error)

    return app
