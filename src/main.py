import asyncio
import logging
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as users_router
from src.api.notifications import router as notifications_router
from src.api.products import router as products_router
from src.exceptions.base import BaseAppHTTPException
from src.handlers.base import base_app_exception_handler

app = FastAPI()


def register_handlers():
    app.add_exception_handler(
        BaseAppHTTPException,
        base_app_exception_handler,
    )


async def main():
    logging.basicConfig(level=logging.INFO)
    register_handlers()
    app.include_router(router=products_router)
    app.include_router(router=users_router)
    app.include_router(router=notifications_router)


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(app, host="0.0.0.0", port=8000)
