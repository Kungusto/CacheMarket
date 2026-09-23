from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from src.exceptions.base import BaseAppException
from src.exceptions.db import DatabaseException, EntityAlreadyExists

_integrity_err_map = {UniqueViolationError: EntityAlreadyExists}


def map_integrity_error(exc: IntegrityError) -> BaseAppException:
    cause = exc.orig.__cause__

    exc_cls = _integrity_err_map.get(type(cause))
    if exc_cls is not None:
        return exc_cls()
    return DatabaseException()
