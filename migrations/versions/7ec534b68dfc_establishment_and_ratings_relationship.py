"""establishment and ratings relationship

Revision ID: 7ec534b68dfc
Revises: 8901de8ad848
Create Date: 2023-09-05 22:00:25.617840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ec534b68dfc'
down_revision = '8901de8ad848'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.add_column(sa.Column('establishment_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_rating_establishment', 'establishment', ['establishment_id'], ['id'])


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('establishment_id')

    # ### end Alembic commands ###
