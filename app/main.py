# app/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging

from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.api.v1.api import api_router
from app.db.database import engine
from app.models import Base

from app.core.exceptions import (
    BaseCustomException,
    base_custom_exception_handler,
    validation_exception_handler,
    http_exception_handler_custom,
    generic_exception_handler,
)
from app.core.middleware import RequestIDMiddleware, LoggingMiddleware

# Setup logging first
setup_logging()
logger = get_logger("main")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.debug_mode}")
    logger.info(f"Database echo: {settings.database_echo}")
    logger.info(f"CORS origins: {settings.cors_origins}")

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}", exc_info=True)
        raise

    yield

    logger.info(f"Shutting down {settings.APP_NAME}")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="FELCO FastAPI Application with comprehensive error handling",
    openapi_url=settings.get_openapi_url(),
    docs_url=settings.get_docs_url(),
    redoc_url=settings.get_redoc_url(),
    lifespan=lifespan,
)

# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)

# Exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(BaseCustomException, base_custom_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler_custom)
app.add_exception_handler(Exception, generic_exception_handler)

# Routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    response_data = {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running",
    }
    if not settings.is_production():
        response_data["environment"] = settings.ENVIRONMENT
        response_data["debug_mode"] = settings.debug_mode
    return response_data


@app.get("/health")
async def health_check():
    response_data = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.APP_VERSION,
    }
    if not settings.is_production():
        response_data["environment"] = settings.ENVIRONMENT
        response_data["debug_mode"] = settings.debug_mode
        response_data["database_echo"] = settings.database_echo
    return response_data


if settings.is_development():

    @app.get("/debug/settings")
    async def debug_settings():
        return {
            "environment": settings.ENVIRONMENT,
            "debug_mode": settings.debug_mode,
            "database_echo": settings.database_echo,
            "log_level": settings.get_log_level(),
            "cors_origins": settings.cors_origins,
            "include_stack_trace": settings.include_stack_trace,
            "show_docs": settings.show_docs,
        }

    @app.get("/debug/exception")
    async def debug_exception():
        raise Exception("This is a test exception for debugging")


@app.on_event("startup")
async def startup_event():
    logger.info("Application startup complete")
    if settings.is_development():
        logger.debug("Debug endpoints available at /debug/*")
        logger.debug(f"Loaded settings: {settings.dict()}")  # 👈 optional
