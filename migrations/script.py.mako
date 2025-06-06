# StudyHub Database Migration Script Template
# This Mako template generates individual migration files for database schema changes.
# Each migration contains upgrade and downgrade functions to apply or revert changes.

"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
# Core migration imports
from alembic import op  # Alembic operations for schema changes
import sqlalchemy as sa  # SQLAlchemy for database types and operations
${imports if imports else ""}  # Additional imports if needed

# Migration metadata - used by Alembic for version tracking
revision = ${repr(up_revision)}  # Current migration revision ID
down_revision = ${repr(down_revision)}  # Previous migration revision ID
branch_labels = ${repr(branch_labels)}  # Branch labels for complex workflows
depends_on = ${repr(depends_on)}  # Dependencies on other migrations


# Upgrade function - applies schema changes to move forward
def upgrade():
    ${upgrades if upgrades else "pass"}  # Schema upgrade operations


# Downgrade function - reverts schema changes to move backward  
def downgrade():
    ${downgrades if downgrades else "pass"}  # Schema downgrade operations
