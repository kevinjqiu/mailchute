"""change from field to sender

Revision ID: 63d21bb114
Revises: 1633023db6f
Create Date: 2014-08-28 00:34:19.990709

"""

# revision identifiers, used by Alembic.
revision = '63d21bb114'
down_revision = '1633023db6f'

from alembic import op


def upgrade():
    op.alter_column(
        'incoming_email',
        'from',
        new_column_name='sender'
    )


def downgrade():
    op.alter_column(
        'incoming_email',
        'sender',
        new_column_name='from'
    )
