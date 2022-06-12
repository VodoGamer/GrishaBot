"""add chats column

Revision ID: 3093d2fc742d
Revises:
Create Date: 2022-06-06 14:41:15.127594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3093d2fc742d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chats",
        sa.Column('chat_id', sa.Integer(), primary_key=True),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('messages', sa.Integer()),
        sa.Column('person_date', sa.DateTime()),
    )


def downgrade():
    op.drop_table("chats")
