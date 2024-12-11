"""Food

Revision ID: 19dce0a2b679
Revises: d1b9ce4b4979
Create Date: 2024-12-10 21:51:17.659256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19dce0a2b679'
down_revision: Union[str, None] = 'd1b9ce4b4979'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('food_place',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('link_map', sa.String(), nullable=True),
    sa.Column('time', sa.String(), nullable=True),
    sa.Column('budget', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('kitchen',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('food_place_kitchen',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('food_place_id', sa.Integer(), nullable=False),
    sa.Column('kitchen_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['food_place_id'], ['food_place.id'], ),
    sa.ForeignKeyConstraint(['kitchen_id'], ['kitchen.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('telegram_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cuisine_preferences', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('interests', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('available_time', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('budget', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('notifications', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.drop_table('food_place_kitchen')
    op.drop_table('kitchen')
    op.drop_table('food_place')
    # ### end Alembic commands ###
