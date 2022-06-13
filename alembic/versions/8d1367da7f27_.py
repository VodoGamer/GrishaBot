"""add casino table

Revision ID: 8d1367da7f27
Revises: e56580d3106e
Create Date: 2022-06-13 00:24:10.510230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d1367da7f27'
down_revision = 'e56580d3106e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "casino",
        sa.Column('chat_id', sa.Integer()),
        sa.Column('user_id', sa.Integer()),
        sa.Column('bet', sa.Integer()),
        sa.Column('feature', sa.Integer()),
    )
    op.create_table(
        "casino_history",
        sa.Column('chat_id', sa.Integer()),
        sa.Column('win_feature', sa.Integer()),
        sa.Column('date', sa.DateTime()),
        sa.Column('time', sa.DateTime()),
    )


def downgrade():
    op.drop_table("casino")
    op.drop_table("casino_history")
