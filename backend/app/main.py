"""Главный файл приложения"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import coins, futures_history
from app.services.background_tasks import background_service
from app.services.binance_service import binance_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Запуск и остановка приложения"""
    background_service.start()

    await background_service.collect_coins_data()

    yield

    background_service.stop()
    await binance_service.close()


# Создание FastAPI приложения
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Платформа для отслеживания и анализа криптовалютных фьючерсов",
    lifespan=lifespan,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(coins.router, prefix="/api")
app.include_router(futures_history.router, prefix="/api")
