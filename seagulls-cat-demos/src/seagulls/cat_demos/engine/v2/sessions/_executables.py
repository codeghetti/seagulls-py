from abc import abstractmethod
from typing import Callable, Protocol


class IExecutable(Protocol):
    @abstractmethod
    def __call__(self) -> None:
        pass


class Executable(IExecutable):

    _cb: Callable[[], None]

    def __init__(self, cb: Callable[[], None]) -> None:
        self._cb = cb

    def __call__(self) -> None:
        self._cb()


executable = Executable
