"""create role_enum type

Revision ID: bff9617642e1
Revises: ac797c4f85c7
Create Date: 2024-02-20 10:45:15.308494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bff9617642e1'
down_revision: Union[str, None] = 'ac797c4f85c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE role_enum AS ENUM('ADMIN', 'USER')")


def downgrade() -> None:
    op.execute("DROP TYPE role_enum")
