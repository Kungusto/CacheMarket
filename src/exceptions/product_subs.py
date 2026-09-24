from fastapi import status

from src.exceptions.base import BaseAppHTTPException


class AlreadySubscribedHTTPException(BaseAppHTTPException):
    message = "Вы уже подписаны на этот товар"
    status_code = status.HTTP_409_CONFLICT
