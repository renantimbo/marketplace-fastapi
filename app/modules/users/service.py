from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserRegister
from app.core.security import verify_password, get_password_hash, create_access_token
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
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        return self.repository.get_all()
    
    def register_user(self, user_data: UserRegister) -> User:
        """Register a new user."""
        # Check if user already exists
        if self.repository.get_by_email(user_data.email):
            raise ValueError("Email already registered")
        
        # Hash password using passlib
        password_hash = get_password_hash(user_data.password)
        
        # Create user
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict["password_hash"] = password_hash
        
        return self.repository.create(user_dict)
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        user = self.repository.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    
    def create_access_token_for_user(self, user: User) -> str:
        """Create access token for user."""
        token_data = {"sub": str(user.id), "email": user.email}
        return create_access_token(token_data)



