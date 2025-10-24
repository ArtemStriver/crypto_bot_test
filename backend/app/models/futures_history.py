"""Модель истории фьючерсов"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.sql import func
from app.db.database import Base


class FuturesHistory(Base):
    __tablename__ = "futures_history"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False, index=True)
    price = Column(Float, nullable=False)
    previous_price = Column(Float, nullable=True)
    price_change = Column(Float, nullable=True)
    price_change_percent = Column(Float, nullable=True, index=True)
    volume = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    __table_args__ = (
        Index('idx_symbol_timestamp', 'symbol', 'timestamp'),
        Index('idx_timestamp_percent', 'timestamp', 'price_change_percent'),
        Index('idx_symbol_percent_time', 'symbol', 'price_change_percent', 'timestamp'),
    )

    def __repr__(self):
        return f"<FuturesHistory(symbol={self.symbol}, price={self.price}, change={self.price_change_percent}%)>"
