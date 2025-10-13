from datetime import datetime, timedelta, date as date_cls
from typing import Optional, List, Dict

from fastapi import APIRouter, Depends, Query

from app.core.responses import OutModel
from app.db.mongodb import get_db
from app.api.v1.routes.auth import get_current_user

router = APIRouter()


def _date_str(d: datetime | date_cls) -> str:
    if isinstance(d, datetime):
        d = d.date()
    return d.isoformat()


@router.get("/summary", response_model=OutModel)
async def summary(date: Optional[str] = Query(None), period: str = Query("day"), user=Depends(get_current_user)):
    db = get_db()
    if not date:
        date = datetime.utcnow().date().isoformat()

    if period == "day":
        filt = {"user_id": str(user["_id"]), "date": date}
    else:
        dt = datetime.strptime(date, "%Y-%m-%d").date()
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        filt = {"user_id": str(user["_id"]), "date": {"$gte": start.isoformat(), "$lte": end.isoformat()}}

    meals = await db.meals.find(filt).to_list(length=500)

    totals = {"calories": 0.0, "protein": 0.0, "carbs": 0.0, "fat": 0.0}
    for m in meals:
        t = m.get("totals", {})
        totals["calories"] += float(t.get("calories", 0))
        totals["protein"] += float(t.get("protein", 0))
        totals["carbs"] += float(t.get("carbs", 0))
        totals["fat"] += float(t.get("fat", 0))

    goal = await db.goals.find_one({"user_id": str(user["_id"])})
    target = goal.get("target_calories") if goal else None

    return OutModel(
        status="success",
        message="Summary",
        data={
            "date": date,
            "period": period,
            "totals": {k: round(v, 2) for k, v in totals.items()},
            "target_calories": target,
            "progress": round((totals["calories"] / target) * 100, 1) if target else None,
        },
    )


@router.get("/trends", response_model=OutModel)
async def trends(range: int = Query(7, ge=1, le=90), user=Depends(get_current_user)):
    db = get_db()
    end = datetime.utcnow().date()
    start = end - timedelta(days=range - 1)

    pipeline = [
        {"$match": {"user_id": str(user["_id"]), "date": {"$gte": start.isoformat(), "$lte": end.isoformat()}}},
        {"$group": {"_id": "$date", "calories": {"$sum": "$totals.calories"}, "protein": {"$sum": "$totals.protein"}, "carbs": {"$sum": "$totals.carbs"}, "fat": {"$sum": "$totals.fat"}}},
        {"$sort": {"_id": 1}},
    ]
    rows = await db.meals.aggregate(pipeline).to_list(length=1000)
    data = [
        {
            "date": r["_id"],
            "calories": round(float(r.get("calories", 0)), 2),
            "protein": round(float(r.get("protein", 0)), 2),
            "carbs": round(float(r.get("carbs", 0)), 2),
            "fat": round(float(r.get("fat", 0)), 2),
        }
        for r in rows
    ]
    return OutModel(status="success", message="Trends", data={"series": data})
