"""
Пакет схем.
Экспортирует все Pydantic схемы для валидации API.
"""

from app.schemas.coin import CoinCreate, CoinResponse, CoinSearchParams
from app.schemas.futures_history import (
    FuturesHistoryCreate,
    FuturesHistoryResponse,
    FuturesHistoryFilter,
    PaginatedFuturesHistory,
)

__all__ = [
    "CoinCreate",
    "CoinResponse",
    "CoinSearchParams",
    "FuturesHistoryCreate",
    "FuturesHistoryResponse",
    "FuturesHistoryFilter",
    "PaginatedFuturesHistory",
]
