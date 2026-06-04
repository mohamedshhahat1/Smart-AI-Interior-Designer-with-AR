from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Smart AI Interior Designer"
    debug: bool = False
    version: str = "1.0.0"

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/smart_interior"
    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_secure: bool = False

    ai_service_url: str = "http://localhost:8001"

    max_upload_size_mb: int = 20
    allowed_image_types: list[str] = ["image/jpeg", "image/png", "image/webp"]

    openai_api_key: str = ""
    google_api_key: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
