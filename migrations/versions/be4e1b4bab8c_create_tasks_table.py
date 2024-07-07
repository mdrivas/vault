"""Create tasks table

Revision ID: be4e1b4bab8c
Revises: 882a81032d79  # Update this to match the latest revision ID from alembic_version table
Create Date: 2024-07-06 <time>

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'be4e1b4bab8c'
down_revision = '882a81032d79'  # Update this line
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('assignee', sa.String(length=100), nullable=False),
        sa.Column('task', sa.String(length=255), nullable=False),
        sa.Column('status', postgresql.ENUM('not_assigned', 'in_progress', 'completed', name='statusenum'), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    # ### end Alembic commands ###