"""rename from field

Revision ID: 3436e24df10
Revises: 1633023db6f
Create Date: 2014-08-27 00:51:39.423550

"""

# revision identifiers, used by Alembic.
revision = '3436e24df10'
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
