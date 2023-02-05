from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class ServiceProvider(Generic[T]):

    _callback: Callable[[], T]

    def __init__(self, callback: Callable[[], T]) -> None:
        self._callback = callback

    def get_service(self) -> T:
        return self._callback()


def provider(callback: Callable[[], T]) -> ServiceProvider[T]:
    return ServiceProvider(callback)
