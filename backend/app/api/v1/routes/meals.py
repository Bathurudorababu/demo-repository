from datetime import datetime, date as date_cls
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from bson import ObjectId

from app.core.responses import OutModel
from app.db.mongodb import get_db
from app.api.v1.routes.auth import get_current_user

router = APIRouter()


class MealCreateIn(BaseModel):
    food_id: str
    quantity: float = 1
    meal_type: str
    date: Optional[str] = None  # YYYY-MM-DD


@router.post("/", response_model=OutModel)
async def create_meal(payload: MealCreateIn, user=Depends(get_current_user)):
    db = get_db()
    try:
        food = await db.foods.find_one({"_id": ObjectId(payload.food_id)})
    except Exception:
        food = None
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    factor = float(payload.quantity or 1)
    item = {
        "food_id": payload.food_id,
        "quantity": factor,
        "calories": round(food["calories"] * factor, 2),
        "protein": round(food["protein"] * factor, 2),
        "carbs": round(food["carbs"] * factor, 2),
        "fat": round(food["fat"] * factor, 2),
        "name": food["name"],
    }
    totals = {
        "calories": item["calories"],
        "protein": item["protein"],
        "carbs": item["carbs"],
        "fat": item["fat"],
    }

    meal_date = payload.date or datetime.utcnow().date().isoformat()
    doc = {
        "user_id": str(user["_id"]),
        "items": [item],
        "meal_type": payload.meal_type,
        "date": meal_date,
        "totals": totals,
        "created_at": datetime.utcnow(),
    }
    result = await db.meals.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return OutModel(status="success", message="Meal logged", data=doc)


@router.get("/", response_model=OutModel)
async def list_meals(date: Optional[str] = Query(None, description="YYYY-MM-DD"), user=Depends(get_current_user)):
    db = get_db()
    filt = {"user_id": str(user["_id"]) }
    if date:
        filt["date"] = date
    meals = await db.meals.find(filt).sort("created_at", -1).to_list(length=100)
    for m in meals:
        m["id"] = str(m.pop("_id"))
    return OutModel(status="success", message="Meals fetched", data={"items": meals})


@router.delete("/{meal_id}", response_model=OutModel)
async def delete_meal(meal_id: str, user=Depends(get_current_user)):
    db = get_db()
    try:
        doc = await db.meals.find_one({"_id": ObjectId(meal_id), "user_id": str(user["_id"])})
    except Exception:
        doc = None
    if not doc:
        raise HTTPException(status_code=404, detail="Meal not found")
    await db.meals.delete_one({"_id": doc["_id"]})
    return OutModel(status="success", message="Meal deleted", data={})
