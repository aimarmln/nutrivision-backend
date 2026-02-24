import uuid
from http import HTTPMethod
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.food_service import FoodService
from app.middlewares.uuid_middleware import validate_uuid_params
from app.schemas.food_schema import FoodsListQueryParams
from app.utils.responses import success_response
from app.utils.validation import validate_image_upload

food_bp = Blueprint('foods', __name__, url_prefix='/api/foods')

@food_bp.route('', methods=[HTTPMethod.GET])
@jwt_required()
def get_foods_list():
    # Validate query parameters
    params = FoodsListQueryParams(**request.args)

    # Call service to get all foods
    result, pagination = FoodService.get_all_foods(params)

    return success_response(
        data=result,
        message='Foods retrieved successfully',
        pagination=pagination,
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
    )
