from http import HTTPStatus, HTTPMethod
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.user_service import UserService
from app.schemas.user_schema import UpdateUserProfileSchema
from app.utils.responses import success_response

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/daily-summary', methods=[HTTPMethod.GET])
@jwt_required()
def get_user_summary():
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Call the service to get user summary
    result = UserService.get_user_summary(user_id)

    return success_response(
        data=result, 
        message='User summary retrieved successfully', 
        status_code=HTTPStatus.OK
    )
    
@user_bp.route('/profile', methods=[HTTPMethod.GET])
@jwt_required()
def get_user_profile():
    # Get user ID from JWT
    user_id = get_jwt_identity()

    # Get user profile
    result = UserService.get_user_profile(user_id)

    return success_response(
        data=result,
        message='User profile retrieved successfully',
        status_code=HTTPStatus.OK
    )

@user_bp.route('/profile', methods=[HTTPMethod.PATCH])
@jwt_required()
def update_user_profile():
    # Get user ID from JWT
    user_id = get_jwt_identity()

    # Validate request body
    raw_data = request.get_json()
    validated_data = UpdateUserProfileSchema(**raw_data)

    # Update user profile
    result = UserService.update_user_profile(user_id, validated_data)

    return success_response(
        data=result,
        message='User profile updated successfully',
        status_code=HTTPStatus.OK
    )
