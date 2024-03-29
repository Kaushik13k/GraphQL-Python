"""initial

Revision ID: 6832130862a2
Revises: 
Create Date: 2024-02-05 22:21:03.289659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6832130862a2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(), nullable=True),
    sa.Column('lastname', sa.VARCHAR(), nullable=True),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('salt', sa.LargeBinary(), nullable=True),
    sa.Column('hash', sa.LargeBinary(), nullable=True),
    sa.Column('phone_number', sa.Integer(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_age'), 'users', ['age'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_first_name'), 'users', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_hash'), 'users', ['hash'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_index(op.f('ix_users_lastname'), 'users', ['lastname'], unique=False)
    op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=False)
    op.create_index(op.f('ix_users_salt'), 'users', ['salt'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_salt'), table_name='users')
    op.drop_index(op.f('ix_users_phone_number'), table_name='users')
    op.drop_index(op.f('ix_users_lastname'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_hash'), table_name='users')
    op.drop_index(op.f('ix_users_first_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_age'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
