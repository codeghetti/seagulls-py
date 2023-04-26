from abc import abstractmethod
from typing import Protocol, TypeAlias, TypeVar

T = TypeVar("T", covariant=True)


class ServiceProvider(Protocol[T]):
    @abstractmethod
    def __call__(self) -> T:
        pass


class Provider(ServiceProvider[T]):
    _callback: ServiceProvider[T]

    def __init__(self, callback: ServiceProvider[T]) -> None:
        self._callback = callback

    def __call__(self) -> T:
        return self._callback()


provider: TypeAlias = Provider
