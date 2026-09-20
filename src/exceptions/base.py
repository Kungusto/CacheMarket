from fastapi import status, HTTPException


class BaseAppException(Exception):
    message: str = "Непредвиденная ошибка приложения"

    def __init__(self, *args, **kwargs):
        super().__init__(self.message, *args, **kwargs)

class BaseAppHTTPException(BaseAppException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, *args, **kwargs):
        super().__init__(self.status_code, *args, **kwargs)