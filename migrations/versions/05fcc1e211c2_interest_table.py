"""Interest Table

Revision ID: 05fcc1e211c2
Revises: 7ec534b68dfc
Create Date: 2023-09-16 06:35:54.062034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05fcc1e211c2'
down_revision = '7ec534b68dfc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('interest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('interest')
    # ### end Alembic commands ###