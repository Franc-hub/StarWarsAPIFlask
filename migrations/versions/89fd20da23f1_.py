"""empty message

Revision ID: 89fd20da23f1
Revises: 227ef1f882cd
Create Date: 2021-06-13 17:12:20.405679

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '89fd20da23f1'
down_revision = '227ef1f882cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'token',
               existing_type=mysql.VARCHAR(length=250),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'token',
               existing_type=mysql.VARCHAR(length=250),
               nullable=False)
    # ### end Alembic commands ###
