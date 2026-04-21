"""add pet profile fields

Revision ID: c1a2b3d4e5f6
Revises: 8d4c8b22f9a1
Create Date: 2026-04-20 18:20:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c1a2b3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "8d4c8b22f9a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("pets", sa.Column("breed", sa.String(), server_default=sa.text("'Mixed Breed'"), nullable=False))
    op.add_column("pets", sa.Column("age", sa.String(), server_default=sa.text("'Adult'"), nullable=False))
    op.add_column("pets", sa.Column("gender", sa.String(), server_default=sa.text("'Female'"), nullable=False))
    op.add_column("pets", sa.Column("vaccinated", sa.Boolean(), server_default=sa.text("0"), nullable=False))
    op.add_column("pets", sa.Column("sterilized", sa.Boolean(), server_default=sa.text("0"), nullable=False))
    op.add_column("pets", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("pets", sa.Column("image_url", sa.String(), nullable=True))
    op.add_column(
        "pets",
        sa.Column("shelter_name", sa.String(), server_default=sa.text("'FurFinds Shelter'"), nullable=False),
    )
    op.add_column("pets", sa.Column("contact_person", sa.String(), server_default=sa.text("'Rescue Team'"), nullable=False))
    op.add_column("pets", sa.Column("phone", sa.String(), nullable=True))
    op.add_column("pets", sa.Column("email", sa.String(), nullable=True))
    op.add_column("pets", sa.Column("city", sa.String(), server_default=sa.text("'Chennai'"), nullable=False))

    op.create_index(op.f("ix_pets_breed"), "pets", ["breed"], unique=False)
    op.create_index(op.f("ix_pets_city"), "pets", ["city"], unique=False)

    # Give legacy rows meaningful profile details for better UX and recommendation quality.
    op.execute(
        """
        UPDATE pets
        SET
            breed = CASE type
                WHEN 'Dog' THEN 'Indie Mix'
                WHEN 'Cat' THEN 'Domestic Shorthair'
                WHEN 'Rabbit' THEN 'Lop Mix'
                ELSE 'Mixed Breed'
            END,
            age = 'Adult',
            gender = 'Female',
            vaccinated = 1,
            sterilized = 0,
            description = COALESCE(description, 'Friendly and adoption-ready companion.'),
            shelter_name = 'FurFinds Shelter',
            contact_person = 'Rescue Team',
            city = 'Chennai'
        """
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_pets_city"), table_name="pets")
    op.drop_index(op.f("ix_pets_breed"), table_name="pets")

    op.drop_column("pets", "city")
    op.drop_column("pets", "email")
    op.drop_column("pets", "phone")
    op.drop_column("pets", "contact_person")
    op.drop_column("pets", "shelter_name")
    op.drop_column("pets", "image_url")
    op.drop_column("pets", "description")
    op.drop_column("pets", "sterilized")
    op.drop_column("pets", "vaccinated")
    op.drop_column("pets", "gender")
    op.drop_column("pets", "age")
    op.drop_column("pets", "breed")
