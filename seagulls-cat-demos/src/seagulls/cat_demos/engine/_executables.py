from abc import abstractmethod

from typing import Protocol, Callable


class IExecutable(Protocol):
    @abstractmethod
    def execute(self) -> None:
        pass


class Executable(IExecutable):

    _cb: Callable[[], None]

    def __init__(self, cb: Callable[[], None]) -> None:
        self._cb = cb

    def execute(self) -> None:
        self._cb()


executable = Executable
