from enum import Enum

class Gender(str, Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    
    def __str__(self) -> str:
        return str(self.value)

class ActivityLevel(str, Enum):
    SEDENTARY = 'Sedentary'
    LIGHTLY_ACTIVE = 'Lightly Active'
    MODERATELY_ACTIVE = 'Moderately Active'
    ACTIVE = 'Active'
    VERY_ACTIVE = 'Very Active'
    
    def __str__(self) -> str:
        return str(self.value)

class MainGoal(str, Enum):
    LOSE_WEIGHT = 'Lose Weight'
    MAINTAIN_WEIGHT = 'Maintain Weight'
    GAIN_WEIGHT = 'Gain Weight'
    
    def __str__(self) -> str:
        return str(self.value)

class BMIStatus(str, Enum):
    UNDERWEIGHT = 'Underweight'
    HEALTHY = 'Healthy'
    OVERWEIGHT = 'Overweight'
    OBESITY_CLASS_I = 'Obesity Class I'
    OBESITY_CLASS_II = 'Obesity Class II'
    
    def __str__(self) -> str:
        return str(self.value)
    