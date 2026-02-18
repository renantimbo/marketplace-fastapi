"""FastAPI dependency functions — wire use cases with their adapters.

This is the composition root for the users HTTP adapter:
concrete implementations are injected here, keeping use cases
and domain code agnostic of FastAPI and SQLAlchemy.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.adapters.outbound.persistence.user_repository import SQLAlchemyUserRepository
from app.adapters.outbound.security.password_hasher import BcryptPasswordHasher
from app.adapters.outbound.security.token_service import JWTTokenService
from app.application.users.dtos import UserDTO
from app.application.users.use_cases import (
    GetUserByIdUseCase,
    ListUsersUseCase,
    LoginUseCase,
    RegisterUserUseCase,
)
from app.domain.users.exceptions import UserNotFoundError
from app.infrastructure.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

# Singletons — stateless, safe to reuse across requests
_password_hasher = BcryptPasswordHasher()
_token_service = JWTTokenService()


#  Use-case factories

def get_register_use_case(db: Session = Depends(get_db)) -> RegisterUserUseCase:
    return RegisterUserUseCase(
        user_repo=SQLAlchemyUserRepository(db),
        password_hasher=_password_hasher,
    )


def get_login_use_case(db: Session = Depends(get_db)) -> LoginUseCase:
    return LoginUseCase(
        user_repo=SQLAlchemyUserRepository(db),
        password_hasher=_password_hasher,
        token_service=_token_service,
    )


def get_list_users_use_case(db: Session = Depends(get_db)) -> ListUsersUseCase:
    return ListUsersUseCase(user_repo=SQLAlchemyUserRepository(db))


# Auth dependencies

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserDTO:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = _token_service.decode_token(token)
    if payload is None:
        raise credentials_exception

    raw_id: str = payload.get("sub")
    if raw_id is None:
        raise credentials_exception

    try:
        user_id = int(raw_id)
    except (ValueError, TypeError):
        raise credentials_exception

    try:
        return GetUserByIdUseCase(user_repo=SQLAlchemyUserRepository(db)).execute(user_id)
    except UserNotFoundError:
        raise credentials_exception


async def get_current_admin_user(current_user: UserDTO = Depends(get_current_user)) -> UserDTO:
    if not current_user.role.value == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user
