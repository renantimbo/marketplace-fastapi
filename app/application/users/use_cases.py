"""Use cases — application services that orchestrate domain logic.

Each use case:
  - Accepts a command (plain dataclass)
  - Delegates to domain ports (interfaces, never concrete adapters)
  - Returns a DTO (plain dataclass)
  - Raises domain exceptions on business rule violations
"""

from typing import List

from app.domain.users.entities import User
from app.domain.users.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from app.domain.users.ports import IPasswordHasher, ITokenService, IUserRepository

from .dtos import LoginCommand, RegisterUserCommand, TokenDTO, UserDTO


def _to_dto(user: User) -> UserDTO:
    return UserDTO(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository, password_hasher: IPasswordHasher) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher

    def execute(self, command: RegisterUserCommand) -> UserDTO:
        if self._user_repo.find_by_email(command.email):
            raise EmailAlreadyRegisteredError(f"Email {command.email} already registered")

        hashed = self._password_hasher.hash(command.password)
        user = User(
            name=command.name,
            email=command.email,
            password_hash=hashed,
            role=command.role,
        )
        saved = self._user_repo.save(user)
        return _to_dto(saved)


class LoginUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        password_hasher: IPasswordHasher,
        token_service: ITokenService,
    ) -> None:
        self._user_repo = user_repo
        self._password_hasher = password_hasher
        self._token_service = token_service

    def execute(self, command: LoginCommand) -> TokenDTO:
        user = self._user_repo.find_by_email(command.email)
        if not user or not self._password_hasher.verify(command.password, user.password_hash):
            raise InvalidCredentialsError("Invalid credentials")

        token = self._token_service.create_token(user_id=user.id, email=user.email)
        return TokenDTO(access_token=token)


class GetUserByIdUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self._user_repo = user_repo

    def execute(self, user_id: int) -> UserDTO:
        user = self._user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")
        return _to_dto(user)


class ListUsersUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self._user_repo = user_repo

    def execute(self) -> List[UserDTO]:
        return [_to_dto(u) for u in self._user_repo.list_all()]
