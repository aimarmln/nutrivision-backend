from http import HTTPStatus, HTTPMethod
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.auth_service import AuthService
from app.schemas.auth_schema import RegisterSchema, LoginSchema, CheckEmailSchema
from app.utils.responses import success_response

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=[HTTPMethod.POST])
def register():
    # Validate request body
    raw_data = request.get_json()
    validated_data = RegisterSchema(**raw_data)

    # Call service to handle registration
    result = AuthService.register(validated_data)

    return success_response(
        data=result,
        message='User registered successfully',
        status_code=HTTPStatus.CREATED
    )

@auth_bp.route('/login', methods=[HTTPMethod.POST])
def login():
    # Validate request body
    raw_data = request.get_json()
    validated_data = LoginSchema(**raw_data)

    # Call service to handle login
    result = AuthService.login(validated_data)

    return success_response(
        data=result,
        message='User logged in successfully',
        status_code=HTTPStatus.OK
    )

@auth_bp.route('/check-email', methods=[HTTPMethod.POST])
def check_email():
    # Validate request body
    raw_data = request.get_json()
    validated_data = CheckEmailSchema(**raw_data)

    # Call service to handle email check
    AuthService.check_email(validated_data)

    return success_response(
        message='Email is available',
        status_code=HTTPStatus.OK
    )

@auth_bp.route('/refresh', methods=[HTTPMethod.POST])
@jwt_required(refresh=True)
def refresh_token():
    # Get current user identity
    current_user_id = get_jwt_identity()

    # Call service to refresh tokens
    result = AuthService.refresh_tokens(current_user_id)

    return success_response(
        data=result,
        message='Access token refreshed successfully',
        status_code=HTTPStatus.OK
    )
