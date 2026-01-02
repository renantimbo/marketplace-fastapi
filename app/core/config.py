from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # CORS
    CORS_ORIGINS: str  # JSON string, will be parsed
    
    # Logging
    LOG_LEVEL: str
    LOG_FORMAT: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_cors_origins(self) -> list[str]:
        """Parse CORS_ORIGINS from JSON string."""
        import json
        try:
            return json.loads(self.CORS_ORIGINS)
        except (json.JSONDecodeError, TypeError):
            return ["*"]


settings = Settings()



