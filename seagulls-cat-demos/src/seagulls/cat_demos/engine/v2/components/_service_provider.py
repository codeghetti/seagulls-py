from abc import abstractmethod
from typing import Callable, Protocol, TypeAlias, TypeVar

T = TypeVar("T")


class ServiceProvider(Protocol[T]):

    @abstractmethod
    def __call__(self) -> T:
        pass


class Provider(ServiceProvider):

    _callback: Callable[[], T]

    def __init__(self, callback: Callable[[], T]) -> None:
        self._callback = callback

    def __call__(self) -> T:
        return self._callback()


provider: TypeAlias = Provider
