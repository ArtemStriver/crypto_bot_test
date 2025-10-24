"""Фоновые задачи для сбора данных"""

import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import delete

from app.db.database import AsyncSessionLocal
from app.services.binance_service import binance_service
from app.services.database_service import db_service
from app.models.futures_history import FuturesHistory
from app.core.config import settings


class BackgroundTaskService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False

    async def collect_coins_data(self):
        """Сбор данных монет (каждые 60 сек)"""
        try:
            # Получаем данные с Binance
            market_data = await binance_service.get_complete_market_data()

            if not market_data:
                return

            # Сохраняем в базу данных
            async with AsyncSessionLocal() as db:
                await db_service.upsert_coins(db, market_data)

        except Exception as e:
            pass

    async def collect_futures_history(self):
        """Сбор истории (каждую секунду)"""
        try:
            # Получаем текущие цены
            prices = await binance_service.get_current_price()

            if not prices:
                return

            # Подготавливаем данные истории
            history_data = []
            for price_data in prices:
                history_data.append({
                    "symbol": price_data["symbol"],
                    "price": float(price_data["price"]),
                    "volume": None,  # Объем недоступен в price endpoint
                })

            # Сохраняем в базу данных (изменения цен вычисляются в db_service)
            async with AsyncSessionLocal() as db:
                await db_service.insert_futures_history(db, history_data)

        except Exception as e:
            pass

    async def cleanup_old_history(self):
        """Удаление истории старше N дней"""
        try:
            async with AsyncSessionLocal() as db:
                cutoff_date = datetime.now() - timedelta(days=settings.HISTORY_RETENTION_DAYS)
                stmt = delete(FuturesHistory).where(FuturesHistory.timestamp < cutoff_date)
                await db.execute(stmt)
                await db.commit()
        except Exception as e:
            pass

    def start(self):
        """Запуск задач"""
        if self.is_running:
            return

        # Планируем сбор монет каждые 60 секунд
        self.scheduler.add_job(
            self.collect_coins_data,
            trigger=IntervalTrigger(seconds=60),
            id="collect_coins",
            name="Collect Coins Data",
            replace_existing=True,
        )

        # Планируем сбор истории фьючерсов каждую секунду
        self.scheduler.add_job(
            self.collect_futures_history,
            trigger=IntervalTrigger(seconds=1),
            id="collect_history",
            name="Collect Futures History",
            replace_existing=True,
        )

        # Планируем очистку старых данных каждый день в 3:00
        self.scheduler.add_job(
            self.cleanup_old_history,
            trigger=CronTrigger(hour=3, minute=0),
            id="cleanup_history",
            name="Cleanup Old History",
            replace_existing=True,
        )

        self.scheduler.start()
        self.is_running = True

    def stop(self):
        """Остановка задач"""
        if not self.is_running:
            return

        self.scheduler.shutdown(wait=False)
        self.is_running = False


# Singleton экземпляр
background_service = BackgroundTaskService()
