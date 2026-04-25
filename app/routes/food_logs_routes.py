from http import HTTPStatus, HTTPMethod
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest
from app.services.food_log_service import FoodLogService
from app.schemas.food_log_schema import CreateFoodLogSchema, UpdateFoodLogSchema
from app.utils.responses import success_response

food_log_bp = Blueprint('food_logs', __name__, url_prefix='/api/food-logs')

@food_log_bp.route('', methods=[HTTPMethod.POST])
@jwt_required()
def create_food_log():
    # Get user ID from JWT
    user_id = get_jwt_identity()

    # Validate request body
    raw_data = request.get_json()
    validated_data = CreateFoodLogSchema(**raw_data)
    
    # Call service to create food log
    result = FoodLogService.create_food_log(user_id, validated_data)

    return success_response(
        data=result,
        message='Food log created successfully',
        status_code=HTTPStatus.CREATED
    )

@food_log_bp.route('/<int:food_log_id>', methods=[HTTPMethod.GET])
@jwt_required()
def get_food_log_detail(food_log_id: int):
    # Validate food log ID
    if food_log_id <= 0:
        return BadRequest('Invalid food log ID. Must be a positive integer.')

    # Get user ID from JWT
    user_id = get_jwt_identity()    

    # Call service to get food log detail
    result = FoodLogService.get_food_log_detail(user_id, food_log_id)

    return success_response(
        data=result,
        message='Food log detail retrieved successfully',
        status_code=HTTPStatus.OK
    )

@food_log_bp.route('/<int:food_log_id>', methods=[HTTPMethod.PUT])
@jwt_required()
def update_food_log(food_log_id: int):
    # Validate food log ID
    if food_log_id <= 0:
        return BadRequest('Invalid food log ID. Must be a positive integer.')
     
    # Get user ID from JWT
    user_id = get_jwt_identity()

    # Validate request body
    raw_data = request.get_json()
    validated_data = UpdateFoodLogSchema(**raw_data)
    
    # Call service to update food log
    result = FoodLogService.update_food_log(user_id, food_log_id, validated_data)

    return success_response(
        data=result,
        message='Food log updated successfully',
        status_code=HTTPStatus.OK
    )

@food_log_bp.route('/<int:food_log_id>', methods=[HTTPMethod.DELETE])
@jwt_required()
def delete_food_log(food_log_id: int):
    # Validate food log ID
    if food_log_id <= 0:
        return BadRequest('Invalid food log ID. Must be a positive integer.')
    
    # Get user ID from JWT
    user_id = get_jwt_identity()

    # Call service to delete food log (soft delete)
    FoodLogService.delete_food_log(user_id, food_log_id)

    return success_response(
        message='Food log deleted successfully',
        status_code=HTTPStatus.OK
    )
