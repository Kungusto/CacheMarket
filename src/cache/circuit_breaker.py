import time


class RedisCircuitBreaker:
    def __init__(self, cooldown: float = 10.0):
        self._cooldown = cooldown
        self._last_failure: float | None = None

    @property
    def is_open(self) -> bool:
        if self._last_failure is None:
            return False
        return time.monotonic() < self._last_failure + self._cooldown

    def record_failure(self) -> None:
        self._last_failure = time.monotonic()

    def record_success(self) -> None:
        self._last_failure = None
