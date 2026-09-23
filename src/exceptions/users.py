from fastapi import status

from src.exceptions.base import BaseAppHTTPException


class EmailAlreadyRegisteredHTTPException(BaseAppHTTPException):
    status_code = status.HTTP_409_CONFLICT
    message = "Аккаунт с такой почтой уже существует"


class UserNotFoundHTTPException(BaseAppHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Пользователь не найден"


class WrongPasswordHTTPException(BaseAppHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Неверный пароль"
