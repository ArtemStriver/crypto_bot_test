"""Схемы для истории фьючерсов"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class FuturesHistoryBase(BaseModel):
    """Базовые поля"""

    symbol: str = Field(..., description="Символ торговой пары")
    price: float = Field(..., description="Текущая цена")
    previous_price: Optional[float] = Field(None, description="Предыдущая цена")
    price_change: Optional[float] = Field(None, description="Абсолютное изменение цены")
    price_change_percent: Optional[float] = Field(None, description="Процентное изменение цены")
    volume: Optional[float] = Field(None, description="Объем торгов")


class FuturesHistoryCreate(FuturesHistoryBase):
    """Создание записи"""

    pass


class FuturesHistoryResponse(FuturesHistoryBase):
    """Ответ с историей"""

    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class FuturesHistoryFilter(BaseModel):
    """Фильтры"""

    symbol: Optional[str] = Field(None, description="Фильтр по символу")
    min_percent_change: Optional[float] = Field(None, description="Минимальное процентное изменение")
    max_percent_change: Optional[float] = Field(None, description="Максимальное процентное изменение")
    start_time: Optional[datetime] = Field(None, description="Начальное время для фильтрации")
    end_time: Optional[datetime] = Field(None, description="Конечное время для фильтрации")
    page: int = Field(1, ge=1, description="Номер страницы для пагинации")
    page_size: int = Field(50, ge=1, le=500, description="Элементов на странице")


class PaginatedFuturesHistory(BaseModel):
    """Ответ с пагинацией"""

    items: list[FuturesHistoryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
