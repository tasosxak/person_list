"""empty message

Revision ID: 55dbf26a2b08
Revises: 
Create Date: 2023-07-04 23:39:59.036839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55dbf26a2b08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('persons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('persons')
    op.drop_table('addresses')
    # ### end Alembic commands ###
