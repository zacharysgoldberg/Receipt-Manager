"""empty message

Revision ID: 93fb8e95f016
Revises: 
Create Date: 2022-04-13 19:22:16.988937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93fb8e95f016'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firstname', sa.Text(), nullable=False),
    sa.Column('lastname', sa.Text(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('totals',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('purchase_totals', sa.Numeric(), nullable=False),
    sa.Column('tax_totals', sa.Numeric(), nullable=False),
    sa.Column('tax_year', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receipts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('purchase_total', sa.Numeric(), nullable=False),
    sa.Column('tax', sa.Numeric(), nullable=False),
    sa.Column('city', sa.Text(), nullable=False),
    sa.Column('state', sa.String(length=2), nullable=False),
    sa.Column('transaction_num', sa.String(length=14), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('total_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['total_id'], ['totals.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('transaction_num')
    )
    op.create_table('users_totals',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('total_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['total_id'], ['totals.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'total_id')
    )
    op.create_table('receipts_totals',
    sa.Column('receipt_id', sa.Integer(), nullable=False),
    sa.Column('total_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['receipt_id'], ['receipts.id'], ),
    sa.ForeignKeyConstraint(['total_id'], ['totals.id'], ),
    sa.PrimaryKeyConstraint('receipt_id', 'total_id')
    )
    op.create_table('users_receipts',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('receipt_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['receipt_id'], ['receipts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'receipt_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_receipts')
    op.drop_table('receipts_totals')
    op.drop_table('users_totals')
    op.drop_table('receipts')
    op.drop_table('totals')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###