import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from app.main import app

@pytest.mark.asyncio
async def test_register_login_meal_flow():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # register
            r = await ac.post("/api/v1/auth/register", json={
                "name":"Alice","email":"alice@example.com","password":"password123"
            })
            assert r.status_code in (200, 400)
            # login
            r = await ac.post("/api/v1/auth/login", json={"email":"alice@example.com","password":"password123"})
            assert r.status_code == 200
            tokens = r.json()["data"]
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}

            # foods
            r = await ac.get("/api/v1/foods", params={"query":"apple"})
            assert r.status_code == 200
            items = r.json()["data"]["items"]
            assert isinstance(items, list)
            food_id = items[0]["id"]

            # create meal
            r = await ac.post("/api/v1/meals", json={"food_id": food_id, "quantity": 1, "meal_type": "breakfast"}, headers=headers)
            assert r.status_code == 200

            # list meals
            r = await ac.get("/api/v1/meals", headers=headers)
            assert r.status_code == 200
            assert isinstance(r.json()["data"]["items"], list)

            # analytics summary
            r = await ac.get("/api/v1/analytics/summary", headers=headers)
            assert r.status_code == 200

            # set goal
            r = await ac.post("/api/v1/goals", json={"goal_type":"maintain"}, headers=headers)
            assert r.status_code == 200

            # get goal
            r = await ac.get("/api/v1/goals", headers=headers)
            assert r.status_code == 200
