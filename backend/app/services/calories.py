from datetime import date
from typing import Literal

ActivityLevel = Literal["sedentary", "light", "moderate", "active", "very_active"]
GoalType = Literal["loss", "maintain", "gain"]


def calculate_bmr_mifflin_st_jeor(gender: str | None, weight_kg: float | None, height_cm: float | None, dob: str | None) -> float:
    if not (weight_kg and height_cm and dob):
        return 0.0
    # Compute age from dob (YYYY-MM-DD)
    try:
        year, month, day = map(int, dob.split("-"))
        birth = date(year, month, day)
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    except Exception:
        age = 30

    # Mifflin-St Jeor
    if gender and gender.lower().startswith("m"):
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return float(max(bmr, 0.0))


def activity_multiplier(level: ActivityLevel | str | None) -> float:
    mapping = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    if level is None:
        return 1.375
    return mapping.get(str(level).lower(), 1.375)


def calorie_adjustment_for_goal(goal: GoalType | str | None) -> int:
    if goal == "loss":
        return -500
    if goal == "gain":
        return 300
    return 0


def estimate_target_calories(gender: str | None, weight_kg: float | None, height_cm: float | None, dob: str | None, activity_level: str | None, goal: GoalType | str | None) -> int:
    bmr = calculate_bmr_mifflin_st_jeor(gender, weight_kg, height_cm, dob)
    tdee = bmr * activity_multiplier(activity_level)
    target = tdee + calorie_adjustment_for_goal(goal)
    return int(max(round(target), 0))
