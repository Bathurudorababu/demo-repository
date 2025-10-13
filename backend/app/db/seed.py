from datetime import datetime
from typing import List

from app.db.mongodb import get_db
from app.core.logging import get_logger
from passlib.context import CryptContext

logger = get_logger(__name__)


COMMON_FOODS = [
    {"name": "Apple", "calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3, "serving_size": "1 medium (182g)"},
    {"name": "Banana", "calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4, "serving_size": "1 medium (118g)"},
    {"name": "Chicken breast", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "serving_size": "100g cooked"},
    {"name": "Rice (white)", "calories": 206, "protein": 4.3, "carbs": 45, "fat": 0.4, "serving_size": "1 cup cooked (158g)"},
    {"name": "Rice (brown)", "calories": 216, "protein": 5.0, "carbs": 45, "fat": 1.8, "serving_size": "1 cup cooked (195g)"},
    {"name": "Oats", "calories": 152, "protein": 5.3, "carbs": 27, "fat": 2.6, "serving_size": "40g dry"},
    {"name": "Egg", "calories": 78, "protein": 6.3, "carbs": 0.6, "fat": 5.3, "serving_size": "1 large (50g)"},
    {"name": "Milk (2%)", "calories": 122, "protein": 8, "carbs": 12, "fat": 5, "serving_size": "1 cup (244g)"},
    {"name": "Almonds", "calories": 164, "protein": 6, "carbs": 6, "fat": 14, "serving_size": "28g (23 nuts)"},
    {"name": "Broccoli", "calories": 55, "protein": 3.7, "carbs": 11, "fat": 0.6, "serving_size": "1 cup chopped (91g)"},
    {"name": "Salmon", "calories": 208, "protein": 20, "carbs": 0, "fat": 13, "serving_size": "100g cooked"},
]


async def seed_database() -> None:
    db = get_db()
    foods_count = await db.foods.count_documents({})
    if foods_count == 0:
        logger.info("Seeding foods collection with common foods")
        await db.foods.insert_many(COMMON_FOODS)

    # Seed a test user if not exists
    existing = await db.users.find_one({"email": "test@example.com"})
    if not existing:
        logger.info("Seeding test user and sample meals")
        pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user = {
            "name": "Test User",
            "email": "test@example.com",
            "password_hash": pwd.hash("password123"),
            "role": "user",
            "gender": "other",
            "dob": "1990-01-01",
            "height_cm": 175,
            "weight_kg": 75,
            "activity_level": "moderate",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        result = await db.users.insert_one(user)
        user_id = str(result.inserted_id)

        # Sample meals
        sample_foods = await db.foods.find({"name": {"$in": ["Apple", "Chicken breast", "Rice (white)"]}}).to_list(length=3)
        food_map = {f["name"]: f for f in sample_foods}
        meals = [
            {
                "user_id": user_id,
                "items": [
                    {"food_id": str(food_map["Apple"]["_id"]), "quantity": 1, "calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3}
                ],
                "meal_type": "breakfast",
                "date": datetime.utcnow().date().isoformat(),
                "totals": {"calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3},
                "created_at": datetime.utcnow(),
            },
            {
                "user_id": user_id,
                "items": [
                    {"food_id": str(food_map["Chicken breast"]["_id"]), "quantity": 1, "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
                    {"food_id": str(food_map["Rice (white)"]["_id"]), "quantity": 1, "calories": 206, "protein": 4.3, "carbs": 45, "fat": 0.4},
                ],
                "meal_type": "lunch",
                "date": datetime.utcnow().date().isoformat(),
                "totals": {"calories": 371, "protein": 35.3, "carbs": 45, "fat": 4.0},
                "created_at": datetime.utcnow(),
            },
        ]
        if meals:
            await db.meals.insert_many(meals)

        # Sample goal
        goal = {
            "user_id": user_id,
            "target_calories": 2200,
            "goal_type": "maintain",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        await db.goals.insert_one(goal)
