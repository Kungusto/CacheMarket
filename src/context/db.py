from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database import async_session_factory
from src.utils.db_manager import DBManager


@asynccontextmanager
async def get_db():
    async with DBManager(session_factory=async_session_factory) as db:
        yield db



