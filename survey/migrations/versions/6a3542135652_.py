"""empty message

Revision ID: 6a3542135652
Revises: 6e33a77848f2
Create Date: 2020-08-20 11:42:43.389423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a3542135652'
down_revision = '6e33a77848f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('baseuser', sa.Column('company_pk', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'baseuser', 'company', ['company_pk'], ['pk'])
    op.add_column('company', sa.Column('author_pk', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'company', 'baseuser', ['author_pk'], ['pk'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'company', type_='foreignkey')
    op.drop_column('company', 'author_pk')
    op.drop_constraint(None, 'baseuser', type_='foreignkey')
    op.drop_column('baseuser', 'company_pk')
    # ### end Alembic commands ###
