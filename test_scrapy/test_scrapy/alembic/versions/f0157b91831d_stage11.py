"""stage11

Revision ID: f0157b91831d
Revises: 25bc0c962e22
Create Date: 2021-10-07 14:26:37.520532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0157b91831d'
down_revision = '25bc0c962e22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('keyword', sa.Column('keyword', sa.String(length=50), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('keyword', 'keyword')
    # ### end Alembic commands ###
