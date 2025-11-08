from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import DATABASE_URL

Base = declarative_base()


class AsyncDatabaseSession:
    _engine = create_async_engine(DATABASE_URL, future=True, echo=True)
    _session_factory = sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)  # noqa

    async def __call__(self):
        async with self._session_factory() as session:  # noqa
            yield session


session = AsyncDatabaseSession()
