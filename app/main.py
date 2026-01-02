import logging
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.infra.db import engine, get_db
from app.infra.redis import get_redis
from app.modules.users.routes import router as users_router

# Setup logging
logger = setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(users_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")


@app.get("/")
def root():
    """Root endpoint."""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Marketplace API"}


@app.get("/health")
def health_check():
    """Health check endpoint - verifies DB and Redis connections."""
    health_status = {
        "status": "healthy",
        "database": "unknown",
        "redis": "unknown"
    }
    
    # Check database connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        health_status["database"] = "connected"
        logger.debug("Database health check: OK")
    except Exception as e:
        health_status["database"] = "disconnected"
        health_status["status"] = "unhealthy"
        logger.error(f"Database health check failed: {str(e)}")
    
    # Check Redis connection
    try:
        redis_client = get_redis()
        redis_client.ping()
        health_status["redis"] = "connected"
        logger.debug("Redis health check: OK")
    except Exception as e:
        health_status["redis"] = "disconnected"
        health_status["status"] = "unhealthy"
        logger.error(f"Redis health check failed: {str(e)}")
    
    status_code = status.HTTP_200_OK if health_status["status"] == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return health_status



