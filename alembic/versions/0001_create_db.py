"""create database file

Revision ID: 0001_create_db
Revises: 
Create Date: 2026-02-21
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Opening a connection will create the SQLite database file if it doesn't exist.
    conn = op.get_bind()
    conn.execute(sa.text('select 1'))


def downgrade():
    # no-op: do not remove database file automatically
    pass
