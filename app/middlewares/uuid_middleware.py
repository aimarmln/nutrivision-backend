from functools import wraps
from uuid import UUID
from werkzeug.exceptions import BadRequest

def validate_uuid_params(*param_names):
    """
    Validate UUID for specified path parameters globally.
    Example usage: @validate_uuid_params('recipe_id', 'food_id')
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for name in param_names:
                value = kwargs.get(name)
                if value is None:
                    continue  # Skip if parameter is not present
                try:
                    kwargs[name] = UUID(str(value))  # Convert to UUID
                except ValueError:
                    raise BadRequest(f"Invalid UUID for '{name}': {value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
