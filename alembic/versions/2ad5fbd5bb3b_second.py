"""second

Revision ID: 2ad5fbd5bb3b
Revises: 8be6e1a71bb0
Create Date: 2024-12-10 14:21:23.180982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ad5fbd5bb3b'
down_revision: Union[str, None] = '8be6e1a71bb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('notifications', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'notifications')
    # ### end Alembic commands ###