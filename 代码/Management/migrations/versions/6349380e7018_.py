"""empty message

Revision ID: 6349380e7018
Revises: 52792cc1f5d4
Create Date: 2020-03-21 22:00:13.291387

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6349380e7018'
down_revision = '52792cc1f5d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('salary', sa.Column('base_salary', sa.Float(precision=10, asdecimal=2), nullable=True))
    op.drop_column('salary', 'base_wage')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('salary', sa.Column('base_wage', mysql.DECIMAL(precision=10, scale=2), nullable=True))
    op.drop_column('salary', 'base_salary')
    # ### end Alembic commands ###
