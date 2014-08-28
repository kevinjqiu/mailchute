"""create incoming email table

Revision ID: 1633023db6f
Revises: None
Create Date: 2014-08-27 00:31:19.855318

"""

# revision identifiers, used by Alembic.
revision = '1633023db6f'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'raw_message',
        sa.Column('raw_message_id', sa.String(32)),
        sa.Column('message', sa.Text),
    )

    op.create_table(
        'incoming_email',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('from', sa.String(255)),
        sa.Column('recipient', sa.String(255)),
        sa.Column('raw_message_id', sa.String(32)),
    )


def downgrade():
    op.drop_table('incoming_email')
    op.drop_table('raw_message')
