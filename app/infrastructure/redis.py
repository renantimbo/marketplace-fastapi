import redis

from app.core.config import settings


def get_redis() -> redis.Redis:
    """Return a Redis client from the configured URL."""
    return redis.from_url(settings.REDIS_URL, decode_responses=True)
