"""JWT implementation of ITokenService."""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from app.core.config import settings
from app.domain.users.ports import ITokenService


class JWTTokenService(ITokenService):
    def create_token(self, user_id: int, email: str) -> str:
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def decode_token(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            return None
