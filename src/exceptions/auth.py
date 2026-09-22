from fastapi import status

from src.exceptions.base import BaseAppHTTPException


class AlreadyLoggedInHTTPException(BaseAppHTTPException):
    status_code = status.HTTP_409_CONFLICT
    message = "Вы уже вошли в систему"

class UnauthorizedHTTPException(BaseAppHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Вы не аутентифицированы"
