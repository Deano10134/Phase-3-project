"""create tables

Revision ID: 0002_create_tables
Revises: 0001_create_db
Create Date: 2026-02-21
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_create_tables'
down_revision = '0001_create_db'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('email', sa.String(255), nullable=True),
    )

    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('completed', sa.Boolean, nullable=True, server_default=sa.text('0')),
        sa.Column('created_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'recurring_tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('interval', sa.String(50), nullable=True),
    )

    op.create_table(
        'timelogs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('task_id', sa.Integer, nullable=False),
        sa.Column('started_at', sa.DateTime, nullable=True),
        sa.Column('duration_hours', sa.Float, nullable=True),
    )


def downgrade():
    op.drop_table('timelogs')
    op.drop_table('recurring_tasks')
    op.drop_table('tasks')
    op.drop_table('projects')
    op.drop_table('users')
