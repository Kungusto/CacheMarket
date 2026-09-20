from typing import AsyncGenerator, Annotated

from fastapi import Depends

from src.database import async_session_factory
from src.utils.db_manager import DBManager
from src.utils.service_manager import ServiceManager


async def get_db_generator() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_factory) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db_generator)]

async def get_service_dep(db = Depends(get_db_generator)) -> ServiceManager:
    return ServiceManager(db=db)

ServiceDep = Annotated[ServiceManager, Depends(get_service_dep)]