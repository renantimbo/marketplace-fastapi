import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infra.db import get_db
from app.modules.users.service import UserService
from app.modules.users.schemas import UserRegister, UserResponse, UserLogin, Token
from app.modules.users.dependencies import get_current_user, get_current_admin_user
from app.modules.users.models import User
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    logger.info(f"Registration attempt for email: {user_data.email}")
    service = UserService(db)
    try:
        user = service.register_user(user_data)
        logger.info(f"User registered successfully: {user.email}")
        return user
    except ValueError as e:
        logger.warning(f"Registration failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    logger.info(f"Profile accessed by user: {current_user.email}")
    return current_user


@router.get("/", response_model=List[UserResponse])
def list_users(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """List all users (admin only)."""
    logger.info(f"Users list accessed by admin: {current_user.email}")
    service = UserService(db)
    users = service.get_all_users()
    return users


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token."""
    logger.info(f"Login attempt for email: {credentials.email}")
    service = UserService(db)
    user = service.authenticate_user(credentials.email, credentials.password)
    if not user:
        logger.warning(f"Login failed for email: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.create_access_token_for_user(user)
    logger.info(f"Login successful for email: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}



