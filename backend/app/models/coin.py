"""Модель монеты"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.sql import func
from app.db.database import Base


class Coin(Base):
    __tablename__ = "coins"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False, unique=True, index=True)
    price = Column(Float, nullable=False)
    volume_24h = Column(Float, nullable=True)
    price_change_24h = Column(Float, nullable=True)
    price_change_percent_24h = Column(Float, nullable=True)
    high_24h = Column(Float, nullable=True)
    low_24h = Column(Float, nullable=True)
    funding_rate = Column(Float, nullable=True)
    open_interest = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    __table_args__ = (
        Index('idx_symbol_created', 'symbol', 'created_at'),
    )

    def __repr__(self):
        return f"<Coin(symbol={self.symbol}, price={self.price})>"
