import os
from typing import Literal

from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache


class BaseAppSettings(BaseSettings):
    app_name: str = "Smart AI Interior Designer"
    version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/smart_interior"
    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = "dev-only-insecure-key-do-not-use-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_secure: bool = False

    ai_service_url: str = "http://localhost:8001"

    max_upload_size_mb: int = 20
    allowed_image_types: list[str] = ["image/jpeg", "image/png", "image/webp"]

    openai_api_key: str = ""
    google_api_key: str = ""

    cors_allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5000",
        "http://localhost:5001",
        "http://localhost:8081",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:8080",
    ]

    model_config = {"env_file": ".env", "case_sensitive": False}


class DevelopmentSettings(BaseAppSettings):
    environment: str = "development"
    debug: bool = True


class ProductionSettings(BaseAppSettings):
    environment: str = "production"
    debug: bool = False
    minio_secure: bool = True

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters in production")
        if "insecure" in v or "change" in v:
            raise ValueError("SECRET_KEY must be changed from the default value in production")
        return v

    @field_validator("database_url")
    @classmethod
    def validate_db_url(cls, v):
        if "postgres:postgres@" in v:
            raise ValueError("Production database must not use default postgres:postgres credentials")
        return v


class TestingSettings(BaseAppSettings):
    environment: str = "testing"
    debug: bool = True
    database_url: str = "sqlite+aiosqlite:///:memory:"
    secret_key: str = "test-secret-key-not-for-production-use-only"


@lru_cache()
def get_settings() -> BaseAppSettings:
    env = os.getenv("ENVIRONMENT", "development").lower()
    if env == "production":
        return ProductionSettings()
    if env == "testing":
        return TestingSettings()
    return DevelopmentSettings()
