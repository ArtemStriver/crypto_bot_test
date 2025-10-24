"""API для работы с монетами"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.database import get_db
from app.schemas.coin import CoinResponse
from app.services.database_service import db_service

router = APIRouter(prefix="/coins", tags=["Монеты"])


@router.get("/", response_model=List[CoinResponse])
async def get_coins(
    query: Optional[str] = Query(None, description="Поисковый запрос для symbol"),
    limit: int = Query(100, ge=1, le=1000, description="Количество результатов"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    db: AsyncSession = Depends(get_db),
):
    """Получить список монет"""
    coins = await db_service.search_coins(db, query=query, limit=limit, offset=offset)
    return coins


@router.get("/search", response_model=List[CoinResponse])
async def search_coins(
    q: str = Query(..., min_length=1, description="Поисковый запрос"),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """Поиск монет"""
    coins = await db_service.search_coins(db, query=q, limit=limit, offset=0)
    return coins
