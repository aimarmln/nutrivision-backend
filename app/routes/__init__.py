from .auth_routes import auth_bp
from .chat_routes import chat_bp
from .comment_routes import comment_bp
from .food_logs_routes import food_log_bp
from .food_routes import food_bp
from .recipe_routes import recipe_bp
from .user_routes import user_bp

__all__ = [
    'auth_bp',
    'chat_bp',
    'comment_bp',
    'food_log_bp',
    'food_bp',
    'recipe_bp',
    'user_bp'
]