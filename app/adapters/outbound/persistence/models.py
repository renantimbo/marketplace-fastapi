"""SQLAlchemy ORM models — outbound persistence adapter.

These are separate from domain entities on purpose:
persistence details (table names, columns, indexes) must not
leak into the domain layer.
"""

from sqlalchemy import Column, DateTime, Enum as SAEnum, Integer, String
from sqlalchemy.sql import func

from app.domain.users.entities import UserRole
from app.infrastructure.db import Base


def _role_values(enum_class):
    return [e.value for e in enum_class]


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(
        SAEnum(
            UserRole,
            name="userrole",
            native_enum=True,
            values_callable=_role_values,
            create_constraint=False,
        ),
        nullable=False,
        default=UserRole.CUSTOMER,
        server_default=UserRole.CUSTOMER.value,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
