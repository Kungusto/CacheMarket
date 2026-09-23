from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.base import BaseAppHTTPException


def base_app_exception_handler(request: Request, exc: BaseAppHTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": {"message": exc.message}}
    )
