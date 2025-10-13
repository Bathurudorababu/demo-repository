import pytest
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from app.main import app

@pytest.mark.asyncio
async def test_root():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            resp = await ac.get("/")
            assert resp.status_code == 200
            data = resp.json()
            assert data["status"] == "success"
