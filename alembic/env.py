import asyncio
from logging import getLogger
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

import sources.models  # noqa
from sources.core.config import DATABASE_URL
from sources.database.base import Base

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
logger = getLogger("alembic.env")


def process_revision_directives(context, revision, directives):
    """
    Удаляет пустые ревизии (если нет изменений в схеме).
    """
    script = directives[0]
    if script.upgrade_ops.is_empty():
        directives[:] = []
        logger.info("No schema changes detected; revision file skipped.")


def run_migrations_offline() -> None:
    """
    Оффлайн-режим миграций — без подключения к БД.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        process_revision_directives=process_revision_directives,
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Синхронный запуск миграций через переданное подключение.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Асинхронный запуск миграций через asyncpg.
    """
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Онлайн-режим миграций — с подключением к БД.
    """
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
