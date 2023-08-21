from abc import abstractmethod
from typing import Callable, Protocol

from seagulls.cat_demos.engine.v2.scenes._frame_client import IStopScenes


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


class QuitGameExecutable(IExecutable):
    _stop: IStopScenes

    def __init__(self, stop: IStopScenes) -> None:
        self._stop = stop

    def execute(self) -> None:
        self._stop.stop()
