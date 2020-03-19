"""empty message

Revision ID: b6d79ffacd20
Revises: 62a793c43c7d
Create Date: 2020-03-13 09:19:16.372302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6d79ffacd20'
down_revision = '62a793c43c7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profiles', sa.Column('fname', sa.String(length=80), nullable=True))
    op.add_column('user_profiles', sa.Column('lname', sa.String(length=80), nullable=True))
    op.add_column('user_profiles', sa.Column('profile_created_on', sa.String(length=255), nullable=True))
    op.drop_column('user_profiles', 'last_name')
    op.drop_column('user_profiles', 'first_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profiles', sa.Column('first_name', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
    op.add_column('user_profiles', sa.Column('last_name', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
    op.drop_column('user_profiles', 'profile_created_on')
    op.drop_column('user_profiles', 'lname')
    op.drop_column('user_profiles', 'fname')
    # ### end Alembic commands ###