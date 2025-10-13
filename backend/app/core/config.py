from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, case_sensitive=False)

    ENVIRONMENT: str = "development"
    TESTING: bool = False

    MONGODB_URI: str = "mongodb://mongo:27017"
    DATABASE_NAME: str = "calorie_tracker"

    JWT_SECRET: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 14

    CORS_ORIGINS: List[AnyHttpUrl] | List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    SEED: bool = True


@lru_cache
def get_settings() -> "Settings":
    return Settings()  # type: ignore[call-arg]


settings = get_settings()