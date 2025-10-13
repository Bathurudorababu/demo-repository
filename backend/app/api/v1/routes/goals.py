from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.responses import OutModel
from app.db.mongodb import get_db
from app.api.v1.routes.auth import get_current_user
from app.services.calories import estimate_target_calories

router = APIRouter()


class GoalIn(BaseModel):
    target_calories: Optional[int] = None
    goal_type: Optional[str] = "maintain"  # loss | maintain | gain


@router.post("/", response_model=OutModel)
async def upsert_goal(payload: GoalIn, user=Depends(get_current_user)):
    db = get_db()
    current = await db.goals.find_one({"user_id": str(user["_id"])})
    target = payload.target_calories
    if target is None:
        target = estimate_target_calories(
            user.get("gender"), user.get("weight_kg"), user.get("height_cm"), user.get("dob"), user.get("activity_level"), payload.goal_type
        )
    doc = {
        "user_id": str(user["_id"]),
        "target_calories": int(target or 0),
        "goal_type": payload.goal_type or "maintain",
        "updated_at": datetime.utcnow(),
    }
    if current:
        await db.goals.update_one({"_id": current["_id"]}, {"$set": doc})
    else:
        doc["created_at"] = datetime.utcnow()
        await db.goals.insert_one(doc)
    return OutModel(status="success", message="Goal saved", data=doc)


@router.get("/", response_model=OutModel)
async def get_goal(user=Depends(get_current_user)):
    db = get_db()
    current = await db.goals.find_one({"user_id": str(user["_id"])})
    if not current:
        return OutModel(status="success", message="No goal set", data={})
    current["id"] = str(current.pop("_id"))
    return OutModel(status="success", message="Goal fetched", data=current)
