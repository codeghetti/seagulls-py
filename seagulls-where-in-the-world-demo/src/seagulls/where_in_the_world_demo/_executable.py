from abc import abstractmethod
from typing import Protocol, Callable


class IExecutable(Protocol):

    @abstractmethod
    def execute(self) -> None:
        pass


class CallbackExecutable(IExecutable):

    _callback: Callable[[], None]

    def __init__(self, callback: Callable[[], None]) -> None:
        self._callback = callback

    def execute(self) -> None:
        self._callback()


def executable(callback: Callable[[], None]) -> CallbackExecutable:
    return CallbackExecutable(callback)
