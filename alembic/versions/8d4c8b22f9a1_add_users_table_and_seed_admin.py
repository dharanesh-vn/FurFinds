"""add users table and seed admin

Revision ID: 8d4c8b22f9a1
Revises: bfdfd83722e5
Create Date: 2026-04-20 17:30:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8d4c8b22f9a1"
down_revision: Union[str, Sequence[str], None] = "bfdfd83722e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("role", sa.String(), server_default=sa.text("'user'"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.execute(
        """
        INSERT INTO users (name, email, phone, city, hashed_password, role)
        VALUES (
            'Admin Dharanesh',
            'admin@furfinds.com',
            NULL,
            NULL,
            '$2b$12$QETyUWikvfqaA/L7Ev71feb8HBGN8hQPPHpQKYLaVhNeRiCorVRtG',
            'admin'
        );
        """
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
