"""init

Revision ID: f776a5dae318
Revises:
Create Date: 2022-06-05 21:27:21.818065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f776a5dae318'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chats",
        sa.Column('chat_id', sa.Integer(), primary_key=True),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('messages', sa.Integer()),
        sa.Column('last_person_send', sa.Integer()),
    )

    op.create_table(
        "settings",
        sa.Column('chat_id', sa.Integer(), sa.ForeignKey("chats.id")),
        sa.Column('setting', sa.Text(), nullable=False),
        sa.Column('alias', sa.Text(), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
    )

    op.create_table(
        "casino",
        sa.Column('chat_id', sa.Integer(), sa.ForeignKey("chats.id")),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('bet', sa.Integer(), nullable=False),
        sa.Column('feature', sa.Integer(), nullable=False),
    )

    op.create_table(
        "casino_history",
        sa.Column('chat_id', sa.Integer(), sa.ForeignKey("chats.id")),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('time', sa.DateTime(), nullable=False),
        sa.Column('win_feature', sa.Text(), nullable=False),
    )

    op.create_table(
        "users",
        sa.Column('chat_id', sa.Integer(), sa.ForeignKey("chats.id")),
        sa.Column('user_id', sa.Integer(), primary_key=True),
        sa.Column('messages', sa.Integer()),
        sa.Column('custom_name', sa.Text()),
        sa.Column('sex_request', sa.Integer()),
        sa.Column('money', sa.Integer()),
        sa.Column('dick_size', sa.Integer()),
        sa.Column('last_dick', sa.Integer()),
        sa.Column('is_admin', sa.Text()),
        sa.Column('bonus_date', sa.Text()),
    )

def downgrade():
    op.drop_table("chats")
    op.drop_table("settings")
    op.drop_table("casino")
    op.drop_table("casino_history")
    op.drop_table("users")
