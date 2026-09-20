from typing import Protocol, Awaitable, Any


class CachedMethod(Protocol):
    def __call__(self, *args, **kwargs) -> Awaitable[Any]: ...
    def invalidate(self, **kwargs) -> Awaitable[None]: ...

