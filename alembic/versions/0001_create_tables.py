"""create initial tables

Revision ID: 0001_create_tables
Revises: 
Create Date: 2026-02-10
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'activity',
        sa.Column('name', sa.String(), primary_key=True),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('schedule', sa.String(), nullable=False),
        sa.Column('max_participants', sa.Integer(), nullable=False),
    )

    op.create_table(
        'student',
        sa.Column('email', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('grade', sa.Integer(), nullable=True),
    )

    op.create_table(
        'activitystudent',
        sa.Column('activity_name', sa.String(), sa.ForeignKey('activity.name'), primary_key=True),
        sa.Column('student_email', sa.String(), sa.ForeignKey('student.email'), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table('activitystudent')
    op.drop_table('student')
    op.drop_table('activity')
