from redis.asyncio import Redis
from redis.backoff import NoBackoff
from redis.retry import Retry

from src.cache.circuit_breaker import RedisCircuitBreaker
from src.config import settings

redis_conn = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    socket_timeout=0.5,
    socket_connect_timeout=0.5,
    retry=Retry(NoBackoff(), retries=0),
)

redis_breaker = RedisCircuitBreaker(cooldown=10.0)
