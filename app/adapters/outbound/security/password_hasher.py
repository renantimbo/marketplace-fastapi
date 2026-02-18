"""Bcrypt implementation of IPasswordHasher."""

from passlib.context import CryptContext

from app.domain.users.ports import IPasswordHasher

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BcryptPasswordHasher(IPasswordHasher):
    def hash(self, plain_password: str) -> str:
        return _pwd_context.hash(plain_password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(plain_password, hashed_password)
