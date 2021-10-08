"""stage7

Revision ID: 77086f932f78
Revises: eff1ac91729f
Create Date: 2021-10-07 12:19:13.719705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77086f932f78'
down_revision = 'eff1ac91729f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quote', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'quote', 'author', ['author_id'], ['author_id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'quote', type_='foreignkey')
    op.drop_column('quote', 'author_id')
    # ### end Alembic commands ###
