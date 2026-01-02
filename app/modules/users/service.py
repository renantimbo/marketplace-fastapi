from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserUpdate
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.modules.users.models import User


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.repository.get_by_email(email)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.repository.get_by_username(username)
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        if self.repository.get_by_email(user_data.email):
            raise ValueError("Email already registered")
        if self.repository.get_by_username(user_data.username):
            raise ValueError("Username already taken")
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["hashed_password"] = hashed_password
        
        return self.repository.create(user_dict)
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user data."""
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        return self.repository.update(user, update_data)
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user."""
        user = self.repository.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_access_token_for_user(self, user: User) -> str:
        """Create access token for user."""
        token_data = {"sub": str(user.id), "username": user.username}
        return create_access_token(token_data)



