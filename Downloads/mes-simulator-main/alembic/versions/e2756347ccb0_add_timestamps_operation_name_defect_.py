"""add_timestamps_operation_name_defect_code

Revision ID: e2756347ccb0
Revises: 
Create Date: 2026-03-29 18:38:54.257849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e2756347ccb0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns only — skip enum renames, they're cosmetic
    op.add_column('work_orders', sa.Column(
        'operation_name', sa.String(100), nullable=True))
    op.add_column('work_orders', sa.Column(
        'actual_start', sa.DateTime(), nullable=True))
    op.add_column('work_orders', sa.Column(
        'actual_end', sa.DateTime(), nullable=True))
    op.add_column('sfcs', sa.Column(
        'defect_code', sa.String(100), nullable=True))


def downgrade() -> None:
    op.drop_column('sfcs', 'defect_code')
    op.drop_column('work_orders', 'actual_end')
    op.drop_column('work_orders', 'actual_start')
    op.drop_column('work_orders', 'operation_name')
