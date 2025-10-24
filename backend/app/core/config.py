"""Настройки приложения"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "Crypto Bot"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "cryptobot"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        """URL для подключения к БД"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    BINANCE_API_KEY: Optional[str] = None
    BINANCE_API_SECRET: Optional[str] = None
    BINANCE_BASE_URL: str = "https://fapi.binance.com"

    COINS_COLLECTION_INTERVAL: int = 60 
    HISTORY_COLLECTION_INTERVAL: int = 1
    HISTORY_RETENTION_DAYS: int = 7  # сколько дней хранить историю

    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
