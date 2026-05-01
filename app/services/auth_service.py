from werkzeug.exceptions import Conflict, Unauthorized, NotFound
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models import User
from app.repositories import UserRepository
from app.schemas.auth_schema import CheckEmailSchema, RegisterSchema, LoginSchema
from app.utils.database import db_commit
from app.utils.user import (
    calculate_age, 
    calculate_bmi, 
    determine_bmi_status, 
    calculate_bmr, 
    calculate_calories_per_day, 
    calculate_macronutrients
)


class AuthService:

    @staticmethod
    def register(data: RegisterSchema):
        # Check if email already exists
        existing_user = UserRepository.find_by_email(data.email)
        if existing_user:
            raise Conflict('Email already registered')
        
        # Calculate user metrics
        birthday_date, age = calculate_age(data.birthday)
        bmi = calculate_bmi(data.height_cm, data.weight_kg)
        bmi_status = determine_bmi_status(bmi)
        bmr = calculate_bmr(data.gender, data.height_cm, data.weight_kg, age)
        calories_per_day = calculate_calories_per_day(
            bmr,
            data.activity_level,
            data.main_goal
        )
        macros = calculate_macronutrients(calories_per_day)

        # Create user object
        user = User(
            email=data.email,
            password=generate_password_hash(data.password),
            name=data.name,
            gender=data.gender,
            birthday=birthday_date,
            age=age,
            height_cm=data.height_cm,
            weight_kg=data.weight_kg,
            activity_level=data.activity_level,
            main_goal=data.main_goal,
            bmr=bmr,
            bmi=bmi,
            bmi_status=bmi_status,
            calories_per_day_kcal=calories_per_day,
            carbohydrates_per_day_g=macros.get('carbohydrates', 0),
            proteins_per_day_g=macros.get('proteins', 0),
            fats_per_day_g=macros.get('fats', 0)
        )

        # Save to DB
        UserRepository.save(user)

        db_commit()

        # Generate JWT tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            'user': {
                'id': user.id,
                'name': user.name,
                'calories_per_day': user.calories_per_day_kcal,
                'proteins_per_day': user.proteins_per_day_g,
                'carbs_per_day': user.carbohydrates_per_day_g,
                'fats_per_day': user.fats_per_day_g,
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    @staticmethod
    def login(data: LoginSchema):
        # Find user by email
        user = UserRepository.find_by_email(data.email)
        if not user:
            raise NotFound('User not found')

        # Verify password
        if not check_password_hash(user.password, data.password):
            raise Unauthorized('Invalid password')

        # Generate JWT tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            'user': {
                'id': user.id,
                'name': user.name,
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    
    @staticmethod
    def check_email(data: CheckEmailSchema):
        # Check if email already exists
        existing_user = UserRepository.find_by_email(data.email)
        if existing_user:
            raise Conflict('Email already registered')
    
    @staticmethod
    def refresh_tokens(user_id: str):
        # Generate new JWT tokens
        access_token = create_access_token(identity=str(user_id))
        refresh_token = create_refresh_token(identity=str(user_id))

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }