from pydantic import BaseModel, EmailStr, Field
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
    # email: Optional[EmailStr] = Field(
    #     default=None,
    #     description="Email user"
    # )
    
    name: Optional[str] = Field(
        default=None,
        description="Nama user"
    )
    birthday: Optional[date] = Field(
        default=None,
        description="Tanggal lahir user (YYYY-MM-DD)"
    )
    height_cm: Optional[float] = Field(
        default=None,
        ge=140,
        le=230,
        description="Tinggi badan dalam cm (140-230 cm)"
    )
    weight_kg: Optional[float] = Field(
        default=None,
        ge=40,
        le=250,
        description="Berat badan dalam kg (40-250 kg)"
    )
    activity_level: Optional[ActivityLevel] = Field(
        default=None,
        description="Level aktivitas (Sedentary, Lightly Active, Moderately Active, Active, Very Active)"
    )
    main_goal: Optional[MainGoal] = Field(
        default=None,
        description="Tujuan utama (Lose Weight, Maintain Weight, Gain Weight)"
    )

