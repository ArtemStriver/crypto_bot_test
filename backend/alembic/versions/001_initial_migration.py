"""Initial migration

Revision ID: 001
Revises:
Create Date: 2025-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create coins table
    op.create_table(
        'coins',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=50), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('volume_24h', sa.Float(), nullable=True),
        sa.Column('price_change_24h', sa.Float(), nullable=True),
        sa.Column('price_change_percent_24h', sa.Float(), nullable=True),
        sa.Column('high_24h', sa.Float(), nullable=True),
        sa.Column('low_24h', sa.Float(), nullable=True),
        sa.Column('funding_rate', sa.Float(), nullable=True),
        sa.Column('open_interest', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_coins_id'), 'coins', ['id'], unique=False)
    op.create_index(op.f('ix_coins_symbol'), 'coins', ['symbol'], unique=True)
    op.create_index('idx_symbol_created', 'coins', ['symbol', 'created_at'], unique=False)

    # Create futures_history table
    op.create_table(
        'futures_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('symbol', sa.String(length=50), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('previous_price', sa.Float(), nullable=True),
        sa.Column('price_change', sa.Float(), nullable=True),
        sa.Column('price_change_percent', sa.Float(), nullable=True),
        sa.Column('volume', sa.Float(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_futures_history_id'), 'futures_history', ['id'], unique=False)
    op.create_index(op.f('ix_futures_history_symbol'), 'futures_history', ['symbol'], unique=False)
    op.create_index(op.f('ix_futures_history_timestamp'), 'futures_history', ['timestamp'], unique=False)
    op.create_index(op.f('ix_futures_history_price_change_percent'), 'futures_history', ['price_change_percent'], unique=False)
    op.create_index('idx_symbol_timestamp', 'futures_history', ['symbol', 'timestamp'], unique=False)
    op.create_index('idx_timestamp_percent', 'futures_history', ['timestamp', 'price_change_percent'], unique=False)
    op.create_index('idx_symbol_percent_time', 'futures_history', ['symbol', 'price_change_percent', 'timestamp'], unique=False)


def downgrade() -> None:
    # Drop futures_history table
    op.drop_index('idx_symbol_percent_time', table_name='futures_history')
    op.drop_index('idx_timestamp_percent', table_name='futures_history')
    op.drop_index('idx_symbol_timestamp', table_name='futures_history')
    op.drop_index(op.f('ix_futures_history_price_change_percent'), table_name='futures_history')
    op.drop_index(op.f('ix_futures_history_timestamp'), table_name='futures_history')
    op.drop_index(op.f('ix_futures_history_symbol'), table_name='futures_history')
    op.drop_index(op.f('ix_futures_history_id'), table_name='futures_history')
    op.drop_table('futures_history')

    # Drop coins table
    op.drop_index('idx_symbol_created', table_name='coins')
    op.drop_index(op.f('ix_coins_symbol'), table_name='coins')
    op.drop_index(op.f('ix_coins_id'), table_name='coins')
    op.drop_table('coins')
