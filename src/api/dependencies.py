from typing import AsyncGenerator, Annotated

from fastapi import Depends, Request

from src.database import async_session_factory
from src.exceptions.auth import UnauthorizedHTTPException
from src.services.auth import AccessTokenService
from src.utils.db_manager import DBManager
from src.utils.service_manager import ServiceManager


async def get_db_generator() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_factory) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db_generator)]

async def get_service_dep(db = Depends(get_db_generator)) -> ServiceManager:
    return ServiceManager(db=db)

ServiceDep = Annotated[ServiceManager, Depends(get_service_dep)]

def get_user_access_token(request: Request) -> str | None:
    access_token = request.cookies.get("access_token", None)
    if access_token is None:
        raise UnauthorizedHTTPException()
    return access_token


def get_user_id(access_token = Depends(get_user_access_token)) -> int:
    decoded_token = AccessTokenService.decode_token(token=access_token)
    user_id_as_str = decoded_token.get("user_id")
    if user_id_as_str is None:
        raise UnauthorizedHTTPException()
    return int(user_id_as_str)

UserIdDep = Annotated[int, Depends(get_user_id)]