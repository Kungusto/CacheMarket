from fastapi import status

from src.exceptions.base import BaseAppHTTPException


class ProductNotFoundHTTPException(BaseAppHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Товар не найден"
