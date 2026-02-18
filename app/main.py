import logging

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.adapters.inbound.http.users.router import router as users_router
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.infrastructure.db import engine
from app.infrastructure.redis import get_redis

logger = setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    logger.info("Debug mode: %s", settings.DEBUG)


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Marketplace API"}


@app.get("/health")
def health_check():
    health_status = {"status": "healthy", "database": "unknown", "redis": "unknown"}

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        health_status["database"] = "connected"
    except Exception as exc:
        health_status["database"] = "disconnected"
        health_status["status"] = "unhealthy"
        logger.error("Database health check failed: %s", exc)

    try:
        get_redis().ping()
        health_status["redis"] = "connected"
    except Exception as exc:
        health_status["redis"] = "disconnected"
        health_status["status"] = "unhealthy"
        logger.error("Redis health check failed: %s", exc)

    return health_status
