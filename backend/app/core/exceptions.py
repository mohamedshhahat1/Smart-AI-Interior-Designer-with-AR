import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class AppError(Exception):
    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    logger.error("AppError: %s | path=%s | code=%s", exc.message, request.url.path, exc.error_code)
    return JSONResponse(
        {"detail": exc.message, "error_code": exc.error_code},
        status_code=exc.status_code,
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.exception("Database error | path=%s", request.url.path)
    return JSONResponse(
        {"detail": "A database error occurred.", "error_code": "DATABASE_ERROR"},
        status_code=500,
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("Validation error | path=%s | errors=%s", request.url.path, exc.errors())
    return JSONResponse(
        {"detail": exc.errors(), "error_code": "VALIDATION_ERROR"},
        status_code=422,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception | path=%s", request.url.path)
    return JSONResponse(
        {"detail": "An unexpected error occurred.", "error_code": "INTERNAL_ERROR"},
        status_code=500,
    )
