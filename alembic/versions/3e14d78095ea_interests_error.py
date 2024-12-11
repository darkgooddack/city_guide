"""interests_error

Revision ID: 3e14d78095ea
Revises: a2d5edebeffc
Create Date: 2024-12-11 12:04:48.479587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e14d78095ea'
down_revision: Union[str, None] = 'a2d5edebeffc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_food_place')
    op.drop_table('user_interests')
    op.alter_column('food_place', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('food_place', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_table('user_interests',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('interest_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['interest_id'], ['interests.id'], name='user_interests_interest_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_interests_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'interest_id', name='user_interests_pkey')
    )
    op.create_table('user_food_place',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('food_place_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['food_place_id'], ['food_place.id'], name='user_food_place_food_place_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_food_place_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'food_place_id', name='user_food_place_pkey')
    )
    # ### end Alembic commands ###
