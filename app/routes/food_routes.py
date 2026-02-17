import uuid
from http import HTTPStatus, HTTPMethod
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.food_service import FoodService
from app.middlewares.uuid_middleware import validate_uuid_params
from app.utils.responses import success_response
from app.utils.validation import validate_image_upload

food_bp = Blueprint('foods', __name__, url_prefix='/api/foods')

@food_bp.route('', methods=[HTTPMethod.GET])
@jwt_required()
def get_foods_list():
    # Get search query parameter
    search_query = request.args.get('q', None)

    # Call service to get all foods
    result = FoodService.get_all_foods(search_query)

    return success_response(
        data=result,
        message='Foods retrieved successfully',
        status_code=HTTPStatus.OK
    )

@food_bp.route('/<food_id>', methods=[HTTPMethod.GET])
@jwt_required()
@validate_uuid_params('food_id')
def get_food_detail(food_id: uuid.UUID):
    # Call service to get food detail
    result = FoodService.get_food_detail(food_id)

    return success_response(
        data=result,
        message='Food detail retrieved successfully',
        status_code=HTTPStatus.OK
    )

@food_bp.route('/detect', methods=[HTTPMethod.POST])
@jwt_required()
def detect_foods():
    # Validate image upload
    image = validate_image_upload('image')

    # Call service to detect foods
    result = FoodService.detect_foods(image)

    return success_response(
        data=result,
        message='Food detection completed successfully',
        status_code=HTTPStatus.OK
    )
