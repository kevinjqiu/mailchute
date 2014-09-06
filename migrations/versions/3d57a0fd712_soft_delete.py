"""soft delete

Revision ID: 3d57a0fd712
Revises: 2a1e3e9b88f
Create Date: 2014-09-06 10:09:38.401055

"""

# revision identifiers, used by Alembic.
revision = '3d57a0fd712'
down_revision = '2a1e3e9b88f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'incoming_email',
        sa.Column('deleted_at', sa.DateTime, default=None)
    )


def downgrade():
    op.drop_dolumn('incoming_email', 'deleted_at')
