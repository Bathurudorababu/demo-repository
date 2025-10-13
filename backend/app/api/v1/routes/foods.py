from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from bson import ObjectId

from app.core.responses import OutModel
from app.db.mongodb import get_db
from app.api.v1.routes.auth import get_current_user

router = APIRouter()


class FoodIn(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float
    serving_size: Optional[str] = None


@router.get("/", response_model=OutModel)
async def search_foods(query: Optional[str] = None):
    db = get_db()
    if query:
        # Prefer text index then fallback regex
        results = await db.foods.find({"$text": {"$search": query}}).to_list(length=20)
        if not results:
            results = await db.foods.find({"name": {"$regex": query, "$options": "i"}}).to_list(length=20)
    else:
        results = await db.foods.find({}).limit(20).to_list(length=20)

    def serialize(doc):
        doc["id"] = str(doc.pop("_id"))
        return doc

    items = [serialize(x) for x in results]
    return OutModel(status="success", message="Foods fetched", data={"items": items})


@router.get("/{food_id}", response_model=OutModel)
async def get_food(food_id: str):
    db = get_db()
    try:
        doc = await db.foods.find_one({"_id": ObjectId(food_id)})
    except Exception:
        doc = None
    if not doc:
        raise HTTPException(status_code=404, detail="Food not found")
    doc["id"] = str(doc.pop("_id"))
    return OutModel(status="success", message="Food fetched", data=doc)


@router.post("/", response_model=OutModel, dependencies=[Depends(get_current_user)])
async def create_food(payload: FoodIn, user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    db = get_db()
    doc = payload.model_dump()
    result = await db.foods.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return OutModel(status="success", message="Food created", data=doc)
