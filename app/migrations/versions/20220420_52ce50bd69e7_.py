"""empty message

Revision ID: 52ce50bd69e7
Revises: 011906cf4749
Create Date: 2022-04-20 18:50:31.986952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52ce50bd69e7'
down_revision = '011906cf4749'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('authenticated', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'authenticated')
    # ### end Alembic commands ###
