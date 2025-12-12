"""Add expires_at column and remove updated_at

Revision ID: 8g5h9i7j2k1l
Revises: 7fed9952043c
Create Date: 2025-12-12 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8g5h9i7j2k1l'
down_revision = '7fed9952043c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add expires_at column
    op.add_column('urls', sa.Column('expires_at', sa.DateTime(), nullable=True))
    # Remove updated_at column if it exists
    try:
        op.drop_column('urls', 'updated_at')
    except:
        pass


def downgrade() -> None:
    # Remove expires_at column
    op.drop_column('urls', 'expires_at')
    # Add back updated_at column
    op.add_column('urls', sa.Column('updated_at', sa.DateTime(), nullable=False))
