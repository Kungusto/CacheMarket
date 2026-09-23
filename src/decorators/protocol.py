from collections.abc import Awaitable
from typing import Any, Protocol


class CachedMethod(Protocol):
    def __call__(self, *args, **kwargs) -> Awaitable[Any]: ...
    def invalidate(self, **kwargs) -> Awaitable[None]: ...
