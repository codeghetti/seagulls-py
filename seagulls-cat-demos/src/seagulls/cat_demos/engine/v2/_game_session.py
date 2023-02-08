from typing import Iterable, Protocol

from abc import abstractmethod

from ._executables import IExecutable, executable


class IProvideSessionFrames(Protocol):
    @abstractmethod
    def items(self) -> Iterable[IExecutable]:
        pass


class GameSession:

    _session_frames: IProvideSessionFrames

    def __init__(self, session_frames: IProvideSessionFrames) -> None:
        self._session_frames = session_frames

    def run(self) -> None:
        for stage in self._session_frames.items():
            stage.execute()


class StandardSessionFrames(IProvideSessionFrames):

    _open_session: IExecutable
    _run_session: IExecutable
    _close_session: IExecutable

    def __init__(
        self,
        open_session: IExecutable,
        run_session: IExecutable,
        close_session: IExecutable,
    ) -> None:
        self._open_session = open_session
        self._run_session = run_session
        self._close_session = close_session

    def items(self) -> Iterable[IExecutable]:
        return tuple([
            self._open_session,
            self._run_session,
            self._close_session,
        ])
