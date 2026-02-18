"""Application-layer DTOs (Data Transfer Objects).

Commands carry input data into use cases.
Read models carry output data out of use cases.
They are plain dataclasses — no framework dependencies.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.users.entities import UserRole


# Commands (input)

@dataclass
class RegisterUserCommand:
    name: str
    email: str
    password: str
    role: UserRole = UserRole.CUSTOMER


@dataclass
class LoginCommand:
    email: str
    password: str


# Read models (output)

@dataclass
class UserDTO:
    id: int
    name: str
    email: str
    role: UserRole
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class TokenDTO:
    access_token: str
    token_type: str = "bearer"
