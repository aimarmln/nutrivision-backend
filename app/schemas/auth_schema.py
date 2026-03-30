from pydantic import BaseModel, EmailStr
from datetime import date
from app.constants.user import ActivityLevel, MainGoal, Gender


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    name: str
    gender: Gender
    birthday: date
    height_cm: float
    weight_kg: float
    activity_level: ActivityLevel
    main_goal: MainGoal

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class CheckEmailSchema(BaseModel):
    email: EmailStr
    