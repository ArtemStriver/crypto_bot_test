"""
Конфигурация окружения Alembic.
Обрабатывает режимы миграции offline и online.
"""

import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
import asyncio

# Добавление родительской директории в Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импорт конфигурации приложения и моделей
from app.core.config import settings
from app.db.database import Base
from app.models import Coin, FuturesHistory  # Импорт всех моделей

# Объект конфигурации Alembic
config = context.config

# Установка URL базы данных из настроек
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Интерпретация конфигурационного файла для логирования Python
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Целевые метаданные для автогенерации
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Запуск миграций в режиме 'offline'.
    Настраивает контекст только с URL, без Engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Execute migrations in online mode."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    Creates an Engine and associates a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = AsyncEngine(
        engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
