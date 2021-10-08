"""stage5

Revision ID: 464bd0f405d6
Revises: 1862fccbc243
Create Date: 2021-10-06 22:12:52.246215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '464bd0f405d6'
down_revision = '1862fccbc243'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('keywords_and_quotes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('keyword_id', sa.Integer(), nullable=False),
    sa.Column('quote_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.keyword_id'], ),
    sa.ForeignKeyConstraint(['quote_id'], ['quote.quote_id'], ),
    sa.PrimaryKeyConstraint('id', 'keyword_id', 'quote_id')
    )
    op.drop_table('association')
    op.add_column('quote', sa.Column('quote', sa.String(length=500), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quote', 'quote')
    op.create_table('association',
    sa.Column('keyword_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quote_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.keyword_id'], name='association_keyword_id_fkey'),
    sa.ForeignKeyConstraint(['quote_id'], ['quote.quote_id'], name='association_quote_id_fkey'),
    sa.PrimaryKeyConstraint('keyword_id', 'quote_id', name='association_pkey')
    )
    op.drop_table('keywords_and_quotes')
    # ### end Alembic commands ###
