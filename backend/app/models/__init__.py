"""
Пакет моделей.
Экспортирует все модели базы данных для удобного импорта.
"""

from app.models.coin import Coin
from app.models.futures_history import FuturesHistory

__all__ = ["Coin", "FuturesHistory"]
