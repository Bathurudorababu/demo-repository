from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_mongo_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo() -> None:
    global _mongo_client, _db
    if _mongo_client is None:
        logger.info("Connecting to MongoDB...")
        _mongo_client = AsyncIOMotorClient(settings.MONGODB_URI)
        _db = _mongo_client[settings.DATABASE_NAME]
        logger.info("Connected to MongoDB")


def get_db() -> AsyncIOMotorDatabase:
    assert _db is not None, "Database is not initialized"
    return _db


async def close_mongo_connection() -> None:
    global _mongo_client
    if _mongo_client is not None:
        logger.info("Closing MongoDB connection...")
        _mongo_client.close()
        _mongo_client = None
        logger.info("MongoDB connection closed")
