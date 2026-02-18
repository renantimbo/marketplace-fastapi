"""Ports — abstract interfaces that the domain exposes.

Primary ports  → called by inbound adapters (HTTP, CLI…)
Secondary ports → implemented by outbound adapters (DB, cache, security…)

The domain never imports concrete adapters; adapters import the domain.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.users.entities import User


class IUserRepository(ABC):
    """Secondary port: persistence contract."""

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    def save(self, user: User) -> User: ...

    @abstractmethod
    def list_all(self) -> List[User]: ...


class IPasswordHasher(ABC):
    """Secondary port: password hashing contract."""

    @abstractmethod
    def hash(self, plain_password: str) -> str: ...

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool: ...


class ITokenService(ABC):
    """Secondary port: JWT token contract."""

    @abstractmethod
    def create_token(self, user_id: int, email: str) -> str: ...

    @abstractmethod
    def decode_token(self, token: str) -> Optional[dict]: ...
