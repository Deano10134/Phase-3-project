"""Initialize database configuration.

Revision ID: 0001_initialize_database
Revises:
Create Date: 2026-03-15
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "0001_initialize_database"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Initialize the database migration chain.

    For SQLite, the database file is created when a write operation occurs.
    This revision intentionally starts the Alembic history separately from
    table creation so the project can demonstrate distinct migration steps.
    """
    op.execute("SELECT 1")


def downgrade():
    """No-op downgrade for database initialization revision."""
    op.execute("SELECT 1")