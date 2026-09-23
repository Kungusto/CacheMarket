import asyncio
import logging
import sys
from pathlib import Path

from aiohttp import ClientSession

sys.path.append(str(Path(__file__).parent.parent))

from src.cache.redis_conn import redis_conn

BASE_URL = "http://127.0.0.1:8000"
logging.basicConfig(level=logging.INFO)


async def test_plural_keys_expiration():
    async with ClientSession(base_url=BASE_URL) as session:
        for i in range(1_000):
            await session.get(url=f"/products/{i}")
        for i in range(1_000):
            print(await redis_conn.ttl(f"product:{i}"))


async def test_stampede_keys():
    async with ClientSession(base_url=BASE_URL) as session:
        tasks = [session.get(url="/products/2") for _ in range(50)]
        results = await asyncio.gather(*tasks)
        print(results)


if __name__ == "__main__":
    asyncio.run(test_stampede_keys())
