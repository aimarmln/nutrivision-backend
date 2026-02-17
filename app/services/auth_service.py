import uuid
from werkzeug.exceptions import Conflict, Unauthorized, NotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import RegisterSchema, LoginSchema

class AuthService:

    @staticmethod
    def register(data: RegisterSchema):
        # Check if email already exists
        existing_user = UserRepository.find_by_email(data.email)
        if existing_user:
            raise Conflict('Email already registered')

        # Create user object
        user = User(
            id=uuid.uuid4(),
            email=data.email,
            password=generate_password_hash(data.password),
        )

        # Save to DB
        saved_user = UserRepository.save(user)

        # Generate JWT tokens
        access_token = create_access_token(identity=str(saved_user.id))
        refresh_token = create_refresh_token(identity=str(saved_user.id))

        return {
            'user': {
                'id': str(saved_user.id),
                'email': saved_user.email
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    @staticmethod
    def login(data: LoginSchema):
        # Find user by email
        user = UserRepository.find_by_email(data.email)
        if not user:
            raise NotFound('User with given email not found')

        # Verify password
        if not check_password_hash(user.password, data.password):
            raise Unauthorized('Password is incorrect')

        # Generate JWT tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            'user': {
                'id': str(user.id),
                'name': user.name,
                'email': user.email
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    @staticmethod
    def refresh_tokens(user_id: str):
        # Generate new JWT tokens
        access_token = create_access_token(identity=str(user_id))
        refresh_token = create_refresh_token(identity=str(user_id))

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }