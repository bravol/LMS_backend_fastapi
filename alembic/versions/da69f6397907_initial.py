"""initial

Revision ID: da69f6397907
Revises: 
Create Date: 2025-07-01 04:29:21.575020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'da69f6397907'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loans', sa.Column('phone_number', sa.String(length=30), nullable=True))
    op.create_foreign_key(None, 'loans', 'users', ['phone_number'], ['phone_number'], ondelete='SET NULL')
    op.drop_column('loans', 'user_phone')
    op.create_index(op.f('ix_transactions_phone_number'), 'transactions', ['phone_number'], unique=False)
    op.create_foreign_key(None, 'transactions', 'users', ['phone_number'], ['phone_number'], ondelete='SET NULL')
    op.drop_column('transactions', 'user_phone')
    op.drop_column('transactions', 'narration')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('narration', mysql.VARCHAR(length=1000), nullable=True))
    op.add_column('transactions', sa.Column('user_phone', mysql.VARCHAR(length=30), nullable=True))
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_index(op.f('ix_transactions_phone_number'), table_name='transactions')
    op.add_column('loans', sa.Column('user_phone', mysql.VARCHAR(length=30), nullable=True))
    op.drop_constraint(None, 'loans', type_='foreignkey')
    op.drop_column('loans', 'phone_number')
    # ### end Alembic commands ###
