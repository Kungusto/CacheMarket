import asyncio
import logging
import random
from functools import wraps, partial
from inspect import signature
from typing import Callable, Awaitable, Any, Literal, Protocol

from pydantic import BaseModel
from redis import RedisError

from src.cache.redis_conn import redis_conn, redis_breaker
from src.decorators.protocol import CachedMethod

_MISS_PLACEHOLDER = "__miss__"

log = logging.getLogger(__name__)

type Fetch = Callable[[], Awaitable[BaseModel | None]]

class SchemaOwner(Protocol):
    schema: type[BaseModel]

LOCK_SUFFIX = ":lock"
LOCK_PLACEHOLDER = "1"
LOCK_TTL = 5
LOCK_MAX_WAIT = 3.0
POLL_INTERVAL = 0.3

def _handle_redis_degradation(
        action: Literal["CREATE", "READ", "DELETE"] = "READ"
):
    actions_map = {
        "CREATE": "записи",
        "READ": "чтения",
        "DELETE": "удаления"
    }
    log.warning("Redis недоступен для %s", actions_map.get(action), exc_info=True)
    redis_breaker.record_failure()

def _map_result(res: BaseModel | None) -> str:
    return  _MISS_PLACEHOLDER if res is None else res.model_dump_json()

async def _get_with_lock(
    repo_inst: SchemaOwner,
    key: str,
    actual_ttl: int,
    fetch: Fetch,
) -> BaseModel | None:
    lock_key = key + LOCK_SUFFIX
    if not redis_breaker.is_open:
        try:
            got_lock = await redis_conn.set(
                name=lock_key,
                value=LOCK_PLACEHOLDER,
                nx=True,
                ex=LOCK_TTL,
            )
        except RedisError:
            _handle_redis_degradation(action="CREATE")
            return await fetch()
    else:
        return await fetch()

    if got_lock:
        try:
            result = await fetch()
            mapped_result = _map_result(result)
            try:
                await redis_conn.set(
                    name=key,
                    value=mapped_result,
                    ex=actual_ttl,
                )
            except RedisError:
                _handle_redis_degradation(action="CREATE")
            return result
        finally:
            try:
                await redis_conn.delete(lock_key)
            except RedisError:
                _handle_redis_degradation(action="DELETE")
    else:
        try:
            waited = 0.0
            while waited < LOCK_MAX_WAIT:
                await asyncio.sleep(POLL_INTERVAL)
                try:
                    cached = await redis_conn.get(key)
                except RedisError:
                    log.warning("Redis недоступен для чтения", exc_info=True)
                    return await fetch()
                if cached is not None:
                    return repo_inst.schema.model_validate_json(cached) if cached != _MISS_PLACEHOLDER else None
                waited += POLL_INTERVAL
        except RedisError:
            _handle_redis_degradation(action="READ")
        return await fetch()


def cache(
    key_format: str,
    ttl: int = 300,
    jitter: int = 30,
    stampede_protection: bool = False,
) -> Callable[[Callable], CachedMethod]:
    def wrapper(func: Callable) -> CachedMethod:
        @wraps(func)
        async def inner(self, *args, **kwargs):
            sig = signature(func)
            bound = sig.bind(self, *args, **kwargs)
            sig_args = bound.arguments
            key = key_format.format(**sig_args)

            actual_ttl = ttl + random.randint(0, jitter)

            fetch = partial(func, self, *args, **kwargs)

            if stampede_protection:
                return await _get_with_lock(
                    key=key,
                    actual_ttl=actual_ttl,
                    fetch=fetch,
                    repo_inst=self
                )

            return await _get_plain(
                actual_ttl=actual_ttl,
                key=key,
                fetch=fetch,
                repo_inst=self
            )

        async def _get_plain(
            repo_inst: SchemaOwner,
            actual_ttl: int,
            key: str,
            fetch: Fetch
        ) -> BaseModel | None:
            cached = None

            if not redis_breaker.is_open:
                try:
                    cached = await redis_conn.get(key)
                except RedisError:
                    redis_breaker.record_failure()
                    log.warning("Redis недоступен для чтения", exc_info=True)

                if cached is not None:
                    if cached == _MISS_PLACEHOLDER:
                        return None
                    return repo_inst.schema.model_validate_json(cached)

            result = await fetch()

            if not redis_breaker.is_open:
                try:
                    if result is None:
                        await redis_conn.set(
                            name=key,
                            value=_MISS_PLACEHOLDER,
                            ex=actual_ttl,
                        )
                    else:
                        await redis_conn.set(
                            name=key,
                            value=result.model_dump_json(),
                            ex=actual_ttl,
                        )
                except RedisError:
                    _handle_redis_degradation(action="CREATE")
            return result

        async def invalidate(**sig_args) -> None:
            key = key_format.format(**sig_args)
            await redis_conn.delete(key)

        inner.invalidate = invalidate
        return inner
    return wrapper
