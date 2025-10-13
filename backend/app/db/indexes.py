from typing import List, Tuple
from pymongo import ASCENDING, TEXT
from app.db.mongodb import get_db


async def ensure_indexes() -> None:
    db = get_db()
    await db.users.create_index("email", unique=True)
    await db.users.create_index("role")

    await db.foods.create_index([("name", TEXT)])

    await db.meals.create_index("user_id")
    await db.meals.create_index("date")

    await db.goals.create_index("user_id", unique=True)

    await db.activities.create_index("user_id")
    await db.activities.create_index("date")

    await db.logs.create_index("user_id")
    await db.logs.create_index("date")
