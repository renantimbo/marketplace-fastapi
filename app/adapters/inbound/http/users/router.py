"""FastAPI router — inbound HTTP adapter for the users bounded context."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.users.dtos import LoginCommand, UserDTO
from app.application.users.use_cases import ListUsersUseCase, LoginUseCase, RegisterUserUseCase
from app.domain.users.exceptions import EmailAlreadyRegisteredError, InvalidCredentialsError

from .dependencies import (
    get_current_admin_user,
    get_current_user,
    get_list_users_use_case,
    get_login_use_case,
    get_register_use_case,
)
from .schemas import RegisterRequest, TokenResponse, UserResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    use_case: RegisterUserUseCase = Depends(get_register_use_case),
):
    logger.info("Registration attempt for email: %s", data.email)
    try:
        user = use_case.execute(data.to_command())
        logger.info("User registered successfully: %s", user.email)
        return UserResponse.from_dto(user)
    except EmailAlreadyRegisteredError as exc:
        logger.warning("Registration failed: %s", exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    use_case: LoginUseCase = Depends(get_login_use_case),
):
    """Login via OAuth2 password flow ('username' field must contain the e-mail)."""
    logger.info("Login attempt for email: %s", form.username)
    try:
        token = use_case.execute(LoginCommand(email=form.username, password=form.password))
        logger.info("Login successful for email: %s", form.username)
        return TokenResponse(access_token=token.access_token, token_type=token.token_type)
    except InvalidCredentialsError:
        logger.warning("Login failed for email: %s", form.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: UserDTO = Depends(get_current_user)):
    logger.info("Profile accessed by user: %s", current_user.email)
    return UserResponse.from_dto(current_user)


@router.get("/", response_model=List[UserResponse])
def list_users(
    current_user: UserDTO = Depends(get_current_admin_user),
    use_case: ListUsersUseCase = Depends(get_list_users_use_case),
):
    logger.info("Users list accessed by admin: %s", current_user.email)
    return [UserResponse.from_dto(u) for u in use_case.execute()]
