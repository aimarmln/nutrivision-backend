from datetime import date
from app.constants.user import ActivityLevel, MainGoal, Gender, BMIStatus

def calculate_age(birthday: date) -> tuple[date, int]:
    today = date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    return birthday, age

# BMI Formula: dividing an adult's weight in kilograms by their height in metres squared, weight(kg)/height(m)^2
# National Health Service UK
def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    height_m = height_cm / 100 
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

# BMI Asia-Pasific Classification: underweight(<18.5 kg/m2), normal weight (18.5–22.9 kg/m2), overweight (23.0–24.9 kg/m2), obesity class I(25.0–29.9 kg/m2), and obesity class II (≥30.0 kg/m2)
# Okawa, Y., Mitsuhashi, T., & Tsuda, T. (2025). The Asia-Pacific Body Mass Index Classification and New-Onset Chronic Kidney Disease in Non-Diabetic Japanese Adults: A Community-Based Longitudinal Study from 1998 to 2023. Biomedicines, 13(2), 373. https://doi.org/10.3390/biomedicines13020373
def determine_bmi_status(bmi: float) -> BMIStatus:
    if bmi < 18.5:
        return BMIStatus.UNDERWEIGHT
    elif bmi < 23.0:
        return BMIStatus.HEALTHY
    elif bmi < 25.0:
        return BMIStatus.OVERWEIGHT
    elif bmi < 30.0:
        return BMIStatus.OBESITY_CLASS_I
    elif bmi >= 30.0:
        return BMIStatus.OBESITY_CLASS_II

# BMR reference: REE (males) = 10 x weight (kg) + 6.25 x height (cm) - 5 x age (y) + 5; REE (females) = 10 x weight (kg) + 6.25 x height (cm) - 5 x age (y) - 161
# Mifflin MD, St Jeor ST, Hill LA, Scott BJ, Daugherty SA, Koh YO. A new predictive equation for resting energy expenditure in healthy individuals. Am J Clin Nutr. 1990 Feb;51(2):241-7. doi: 10.1093/ajcn/51.2.241. PMID: 2305711. 
def calculate_bmr(gender: Gender, height_cm: float, weight_kg: float, age: int) -> float:
    if gender == Gender.MALE:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender == Gender.FEMALE:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return bmr

def calculate_calories_per_day(bmr: float, activity_level: ActivityLevel, main_goals: MainGoal) -> float:
    # TDEE: Sedentary = BMR x 1.2, Lightly Active = BMR x 1.375, Moderately Active = BMR x 1.55, Very Active = BMR x 1.725, Extra Active = BMR x 1.9
    # Athlean-X
    activity_factors = {
        ActivityLevel.SEDENTARY: 1.2,
        ActivityLevel.LIGHTLY_ACTIVE: 1.375,
        ActivityLevel.MODERATELY_ACTIVE: 1.55,
        ActivityLevel.ACTIVE: 1.725,
        ActivityLevel.VERY_ACTIVE: 1.9
    }

    tdee = bmr * activity_factors.get(activity_level) 
    
    # User goals
    calories_per_day = tdee
    if main_goals == MainGoal.MAINTAIN_WEIGHT:
        calories_per_day = tdee
    elif main_goals == MainGoal.LOSE_WEIGHT:
        # Calorie deficit for weight loss: 500-750 kcal, we use 500 kcal for deficit
        # Kim JY. Optimal Diet Strategies for Weight Loss and Weight Loss Maintenance. J Obes Metab Syndr. 2021 Mar 30;30(1):20-31. doi: 10.7570/jomes20065. PMID: 33107442; PMCID: PMC8017325.
        calories_per_day = tdee - 500
    elif main_goals == MainGoal.GAIN_WEIGHT:
        # Calorie surplus for weight gain: ~1500-2000 Kj/day or ~359-478 kcal, we use 350 kcal for surplus
        # Slater GJ, Dieter BP, Marsh DJ, Helms ER, Shaw G, Iraki J. Is an Energy Surplus Required to Maximize Skeletal Muscle Hypertrophy Associated With Resistance Training. Front Nutr. 2019 Aug 20;6:131. doi: 10.3389/fnut.2019.00131. PMID: 31482093; PMCID: PMC6710320.
        calories_per_day = tdee + 350

    return round(calories_per_day)

# Diet macros: 40-50% carbs, 30% protein, 20-30% fat, we use 40% carbs, 30% protein, 30% fat
# Albert Abayev, dietilian at Cedars-Sinai. (2022). 
def calculate_macronutrients(calories_per_day: float) -> dict[str, float]:
    carbohydrates = (0.4 * calories_per_day) / 4  # 1g karbohidrat = 4 kcal
    proteins = (0.3 * calories_per_day) / 4  # 1g protein = 4 kcal
    fats = (0.3 * calories_per_day) / 9  # 1g    lemak = 9 kcal
    return {
        'carbohydrates': round(carbohydrates, 1),
        'proteins': round(proteins, 1),
        'fats': round(fats, 1)
    }
