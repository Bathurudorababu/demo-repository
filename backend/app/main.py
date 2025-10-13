from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import get_logger
from app.core.responses import OutModel
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.db.indexes import ensure_indexes
from app.db.seed import seed_database
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.foods import router as foods_router
from app.api.v1.routes.meals import router as meals_router
from app.api.v1.routes.goals import router as goals_router
from app.api.v1.routes.analytics import router as analytics_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    await ensure_indexes()
    if settings.SEED:
        await seed_database()
    yield
    await close_mongo_connection()


app = FastAPI(title="Calorie Tracker API", version="1.0.0", lifespan=lifespan)

# Normalize CORS origins from env (comma-separated string or list)
_origins = settings.CORS_ORIGINS
if isinstance(_origins, str):
    _origins = [o.strip() for o in _origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=OutModel)
async def root():
    return OutModel(status="success", message="Calorie Tracker API is running", data={})


# API Routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(foods_router, prefix="/api/v1/foods", tags=["foods"])
app.include_router(meals_router, prefix="/api/v1/meals", tags=["meals"])
app.include_router(goals_router, prefix="/api/v1/goals", tags=["goals"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["analytics"])