"""API для работы с историей фьючерсов"""

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
import math

from app.db.database import get_db
from app.schemas.futures_history import (
    FuturesHistoryFilter,
    PaginatedFuturesHistory,
    FuturesHistoryResponse,
)
from app.services.database_service import db_service

router = APIRouter(prefix="/futures-history", tags=["История фьючерсов"])


@router.post("/filter", response_model=PaginatedFuturesHistory)
async def filter_futures_history(
    filters: FuturesHistoryFilter = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Фильтрация истории"""
    records, total = await db_service.filter_futures_history(db, filters)

    total_pages = math.ceil(total / filters.page_size) if total > 0 else 0

    return PaginatedFuturesHistory(
        items=[FuturesHistoryResponse.model_validate(record) for record in records],
        total=total,
        page=filters.page,
        page_size=filters.page_size,
        total_pages=total_pages,
    )
