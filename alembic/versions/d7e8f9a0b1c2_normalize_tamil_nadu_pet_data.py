"""normalize tamil nadu pet data

Revision ID: d7e8f9a0b1c2
Revises: c1a2b3d4e5f6
Create Date: 2026-04-20 18:45:00.000000
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "d7e8f9a0b1c2"
down_revision: Union[str, Sequence[str], None] = "c1a2b3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE pets
        SET city = CASE (id % 5)
            WHEN 0 THEN 'Chennai'
            WHEN 1 THEN 'Coimbatore'
            WHEN 2 THEN 'Madurai'
            WHEN 3 THEN 'Erode'
            ELSE 'Salem'
        END
        """
    )
    op.execute(
        """
        UPDATE pets
        SET phone = '+919876543210'
        WHERE phone IS NULL OR TRIM(phone) = ''
        """
    )
    op.execute(
        """
        UPDATE pets
        SET phone = '+91' || TRIM(REPLACE(phone, '+', ''))
        WHERE phone IS NOT NULL AND TRIM(phone) <> '' AND phone NOT LIKE '+91%'
        """
    )


def downgrade() -> None:
    op.execute("UPDATE pets SET city = 'Chennai'")
