"""HTTP-layer Pydantic schemas.

These are pure I/O contracts for the HTTP adapter.
They know how to convert to/from application-layer DTOs/commands
but are never imported by the domain or application layers.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.application.users.dtos import LoginCommand, RegisterUserCommand, UserDTO
from app.domain.users.entities import UserRole


# Request bodies

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = UserRole.CUSTOMER

    def to_command(self) -> RegisterUserCommand:
        return RegisterUserCommand(
            name=self.name,
            email=self.email,
            password=self.password,
            role=self.role,
        )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    def to_command(self) -> LoginCommand:
        return LoginCommand(email=self.email, password=self.password)


# Response bodies


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_dto(cls, dto: UserDTO) -> "UserResponse":
        return cls(
            id=dto.id,
            name=dto.name,
            email=dto.email,
            role=dto.role,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
