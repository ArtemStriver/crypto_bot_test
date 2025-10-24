"""Работа с базой данных"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc
from sqlalchemy.dialects.postgresql import insert
from typing import List, Optional, Dict
from datetime import datetime

from app.models.coin import Coin
from app.models.futures_history import FuturesHistory
from app.schemas.futures_history import FuturesHistoryFilter


class DatabaseService:
    @staticmethod
    async def upsert_coins(db: AsyncSession, coins_data: List[Dict]) -> int:
        """Вставить или обновить монеты в БД"""
        try:
            if not coins_data:
                return 0

            stmt = insert(Coin).values(coins_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=['symbol'],
                set_={
                    'price': stmt.excluded.price,
                    'volume_24h': stmt.excluded.volume_24h,
                    'price_change_24h': stmt.excluded.price_change_24h,
                    'price_change_percent_24h': stmt.excluded.price_change_percent_24h,
                    'high_24h': stmt.excluded.high_24h,
                    'low_24h': stmt.excluded.low_24h,
                    'funding_rate': stmt.excluded.funding_rate,
                    'open_interest': stmt.excluded.open_interest,
                    'updated_at': func.now(),
                }
            )

            await db.execute(stmt)
            await db.commit()

            return len(coins_data)

        except Exception as e:
            await db.rollback()
            return 0

    @staticmethod
    async def get_latest_coin_price(db: AsyncSession, symbol: str) -> Optional[float]:
        """Получить последнюю цену"""
        try:
            stmt = select(Coin.price).where(Coin.symbol == symbol).order_by(desc(Coin.updated_at)).limit(1)
            result = await db.execute(stmt)
            price = result.scalar_one_or_none()
            return price

        except Exception as e:
            return None

    @staticmethod
    async def insert_futures_history(db: AsyncSession, history_data: List[Dict]) -> int:
        """Сохранить историю в БД"""
        try:
            if not history_data:
                return 0

            # Вычисляем изменения цен
            for item in history_data:
                symbol = item['symbol']
                current_price = item['price']

                # Получаем предыдущую цену
                previous_price = await DatabaseService.get_latest_coin_price(db, symbol)

                if previous_price:
                    item['previous_price'] = previous_price
                    item['price_change'] = current_price - previous_price
                    item['price_change_percent'] = ((current_price - previous_price) / previous_price) * 100
                else:
                    item['previous_price'] = None
                    item['price_change'] = 0
                    item['price_change_percent'] = 0

            stmt = insert(FuturesHistory).values(history_data)
            await db.execute(stmt)
            await db.commit()

            return len(history_data)

        except Exception as e:
            await db.rollback()
            return 0

    @staticmethod
    async def search_coins(
        db: AsyncSession,
        query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Coin]:
        """Поиск монет"""
        try:
            stmt = select(Coin).order_by(desc(Coin.updated_at))

            if query:
                stmt = stmt.where(Coin.symbol.ilike(f"%{query}%"))

            stmt = stmt.limit(limit).offset(offset)

            result = await db.execute(stmt)
            coins = result.scalars().all()

            return coins

        except Exception as e:
            return []

    @staticmethod
    async def filter_futures_history(
        db: AsyncSession,
        filters: FuturesHistoryFilter
    ) -> tuple[List[FuturesHistory], int]:
        """Фильтрация истории"""
        try:
            # Базовый запрос
            stmt = select(FuturesHistory).order_by(desc(FuturesHistory.timestamp))
            count_stmt = select(func.count(FuturesHistory.id))

            # Применяем фильтры
            conditions = []

            if filters.symbol:
                conditions.append(FuturesHistory.symbol.ilike(f"%{filters.symbol}%"))

            if filters.min_percent_change is not None:
                conditions.append(FuturesHistory.price_change_percent >= filters.min_percent_change)

            if filters.max_percent_change is not None:
                conditions.append(FuturesHistory.price_change_percent <= filters.max_percent_change)

            if filters.start_time:
                conditions.append(FuturesHistory.timestamp >= filters.start_time)

            if filters.end_time:
                conditions.append(FuturesHistory.timestamp <= filters.end_time)

            if conditions:
                stmt = stmt.where(and_(*conditions))
                count_stmt = count_stmt.where(and_(*conditions))

            # Получаем общее количество
            total_result = await db.execute(count_stmt)
            total = total_result.scalar_one()

            # Применяем пагинацию
            offset = (filters.page - 1) * filters.page_size
            stmt = stmt.limit(filters.page_size).offset(offset)

            # Выполняем запрос
            result = await db.execute(stmt)
            records = result.scalars().all()

            return records, total

        except Exception as e:
            return [], 0


# Singleton экземпляр
db_service = DatabaseService()
