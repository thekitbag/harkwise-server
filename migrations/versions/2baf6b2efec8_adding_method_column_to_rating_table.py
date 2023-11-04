"""adding method column to rating table

Revision ID: 2baf6b2efec8
Revises: 55cab8e7ac01
Create Date: 2023-11-04 14:18:04.035867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2baf6b2efec8'
down_revision = '55cab8e7ac01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rating', sa.Column('method', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rating', 'method')
    # ### end Alembic commands ###