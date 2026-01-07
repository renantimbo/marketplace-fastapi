"""Create users table and role enum

Revision ID: 2ce111ec0f60
Revises: 
Create Date: 2026-01-06 16:28:00.464909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '2ce111ec0f60'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    userrole_enum_create = postgresql.ENUM(
        "admin", "seller", "customer",
        name="userrole",
    )
    userrole_enum_create.create(bind, checkfirst=True)

    userrole_enum = postgresql.ENUM(
        "admin", "seller", "customer",
        name="userrole",
        create_type=False,
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("role", userrole_enum, nullable=False, server_default="customer"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
    )

    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_id", "users", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_users_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    userrole_enum = postgresql.ENUM(
        "admin", "seller", "customer",
        name="userrole",
    )
    userrole_enum.drop(bind, checkfirst=True)
