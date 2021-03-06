"""adding about me and last seen to profile page

Revision ID: 51a9abc718da
Revises: 694aefb6345b
Create Date: 2020-09-19 19:11:46.515384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51a9abc718da'
down_revision = '694aefb6345b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=250), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
