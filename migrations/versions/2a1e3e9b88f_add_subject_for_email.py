"""add subject for email

Revision ID: 2a1e3e9b88f
Revises: 1633023db6f
Create Date: 2014-09-01 19:20:20.578645

"""

# revision identifiers, used by Alembic.
revision = '2a1e3e9b88f'
down_revision = '1633023db6f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'incoming_email',
        sa.Column('subject', sa.String(255))
    )


def downgrade():
    op.drop_column('incoming_email', 'subject')
