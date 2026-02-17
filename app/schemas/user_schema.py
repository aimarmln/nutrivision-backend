from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from app.constants.user import ActivityLevel, MainGoal, Gender

class CompleteUserProfileSchema(BaseModel):
    name: str
    gender: Gender
    birthday: date
    height_cm: float
    weight_kg: float
    activity_level: ActivityLevel
    main_goal: MainGoal

class UpdateUserProfileSchema(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    gender: Optional[Gender] = None
    birthday: Optional[date] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[ActivityLevel] = None
    main_goal: Optional[MainGoal] = None

