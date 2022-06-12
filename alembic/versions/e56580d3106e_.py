"""add settings column

Revision ID: e56580d3106e
Revises: 03109d7d3e85
Create Date: 2022-06-06 20:05:26.860568

"""
from alembic import op
import sqlalchemy as sa
import sqlite3 as sq


# revision identifiers, used by Alembic.
revision = 'e56580d3106e'
down_revision = '03109d7d3e85'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "settings",
        sa.Column('chat_id', sa.Integer()),
        sa.Column('setting_id', sa.Integer()),
        sa.Column('title', sa.Text()),
        sa.Column('value', sa.Integer()),
        sa.Column('boolable', sa.Integer())
    )


def downgrade():
    op.drop_table("settings")
