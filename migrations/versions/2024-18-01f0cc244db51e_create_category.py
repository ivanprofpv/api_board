"""create category

Revision ID: f0cc244db51e
Revises: fcc493da769b
Create Date: 2024-01-18 21:41:45.002216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0cc244db51e'
down_revision: Union[str, None] = 'fcc493da769b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
