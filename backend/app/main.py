import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy.exc import SQLAlchemyError

from backend.app.core.config import get_settings
from backend.app.core.logging_config import configure_logging
from backend.app.core.limiter import limiter
from backend.app.core.exceptions import (
    AppError,
    app_error_handler,
    sqlalchemy_error_handler,
    validation_error_handler,
    unhandled_exception_handler,
)
from backend.app.core.middleware import request_logging_middleware
from backend.app.api.routes import (
    auth, room, design, furniture, cost, house,
    lighting, feng_shui, seasonal, pet_friendly, walkthrough_3d,
    assistant, ar, media,
)

configure_logging()
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Backend starting | env=%s debug=%s", settings.environment, settings.debug)
    yield
    logger.info("Backend shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI-Powered Room Redesign with AR Visualization, Furniture Recommendation, and Cost Estimation",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=request_logging_middleware)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(room.router, prefix=API_PREFIX)
app.include_router(design.router, prefix=API_PREFIX)
app.include_router(furniture.router, prefix=API_PREFIX)
app.include_router(cost.router, prefix=API_PREFIX)
app.include_router(house.router, prefix=API_PREFIX)
app.include_router(lighting.router, prefix=API_PREFIX)
app.include_router(feng_shui.router, prefix=API_PREFIX)
app.include_router(seasonal.router, prefix=API_PREFIX)
app.include_router(pet_friendly.router, prefix=API_PREFIX)
app.include_router(walkthrough_3d.router, prefix=API_PREFIX)
app.include_router(assistant.router, prefix=API_PREFIX)
app.include_router(ar.router, prefix=API_PREFIX)
app.include_router(media.router, prefix=API_PREFIX)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
