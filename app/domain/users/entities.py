from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    CUSTOMER = "customer"


@dataclass
class User:
    """Core domain entity — zero external dependencies."""

    name: str
    email: str
    password_hash: str
    role: UserRole = UserRole.CUSTOMER
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN
