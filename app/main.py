from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.modules.users.routes import router as users_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(users_router, prefix="/api")


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Welcome to Marketplace API"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}



