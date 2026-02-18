"""SQLAlchemy implementation of IUserRepository.

Maps between the ORM model (persistence concern) and the domain
entity (business concern) so the domain stays framework-free.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.users.entities import User
from app.domain.users.ports import IUserRepository

from .models import UserModel


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    # Mapping helpers

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password_hash=model.password_hash,
            role=model.role,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # IUserRepository

    def find_by_id(self, user_id: int) -> Optional[User]:
        model = self._session.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(model) if model else None

    def find_by_email(self, email: str) -> Optional[User]:
        model = self._session.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(model) if model else None

    def save(self, user: User) -> User:
        model = UserModel(
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return self._to_entity(model)

    def list_all(self) -> List[User]:
        return [self._to_entity(m) for m in self._session.query(UserModel).all()]
