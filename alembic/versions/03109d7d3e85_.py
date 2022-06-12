"""add accounts column

Revision ID: 03109d7d3e85
Revises: 3093d2fc742d
Create Date: 2022-06-06 14:44:09.388607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03109d7d3e85'
down_revision = '3093d2fc742d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "accounts",
        sa.Column('chat_id', sa.Integer()),
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('is_admin', sa.Integer()),
        sa.Column('custom_name', sa.Text()),
        sa.Column('messages', sa.Integer()),
        sa.Column('sex_request', sa.Integer()),
        sa.Column('money', sa.Integer()),
        sa.Column('bonus_date', sa.DateTime()),
        sa.Column('dick_size', sa.Integer()),
        sa.Column('dick_date', sa.DateTime()),
    )


def downgrade():
    op.drop_table("accounts")
