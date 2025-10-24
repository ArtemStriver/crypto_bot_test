"""Схемы для монет"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CoinBase(BaseModel):
    """Базовые поля"""

    symbol: str = Field(..., description="Символ торговой пары, например, BTCUSDT")
    price: float = Field(..., description="Текущая цена")
    volume_24h: Optional[float] = Field(None, description="Объем торгов за 24 часа")
    price_change_24h: Optional[float] = Field(None, description="Изменение цены за 24 часа")
    price_change_percent_24h: Optional[float] = Field(None, description="Процентное изменение цены за 24 часа")
    high_24h: Optional[float] = Field(None, description="Максимальная цена за 24 часа")
    low_24h: Optional[float] = Field(None, description="Минимальная цена за 24 часа")
    funding_rate: Optional[float] = Field(None, description="Текущая ставка финансирования")
    open_interest: Optional[float] = Field(None, description="Общий открытый интерес")


class CoinCreate(CoinBase):
    """Создание монеты"""

    pass


class CoinResponse(CoinBase):
    """Ответ с монетой"""

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CoinSearchParams(BaseModel):
    """Параметры поиска"""

    query: Optional[str] = Field(None, description="Поисковый запрос для символа")
    limit: int = Field(100, ge=1, le=1000, description="Количество результатов")
    offset: int = Field(0, ge=0, description="Смещение для пагинации")
