"""empty message

Revision ID: 3cdf073f3dbc
Revises: b462d01ee5b9
Create Date: 2022-02-16 10:01:35.570052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cdf073f3dbc'
down_revision = 'b462d01ee5b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('childcomment', sa.Column('username', sa.String(length=360), nullable=True))
    op.add_column('comment', sa.Column('username', sa.String(length=360), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'username')
    op.drop_column('childcomment', 'username')
    # ### end Alembic commands ###