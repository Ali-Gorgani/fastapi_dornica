"""delete blacklist model

Revision ID: d65f30c0255b
Revises: a6fc6aefe7ac
Create Date: 2024-02-21 10:17:34.178256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd65f30c0255b'
down_revision: Union[str, None] = 'a6fc6aefe7ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='blacklist_tokens_pkey'),
    sa.UniqueConstraint('token', name='blacklist_tokens_token_key')
    )
    # ### end Alembic commands ###