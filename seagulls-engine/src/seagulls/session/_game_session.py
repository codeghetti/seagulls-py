from abc import ABC, abstractmethod
from typing import Protocol


class IStartGameSessions(Protocol):
    @abstractmethod
    def start(self) -> None:
        pass


class IStopGameSessions(Protocol):
    @abstractmethod
    def wait_for_completion(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass


class IGameSession(IStartGameSessions, IStopGameSessions, Protocol):
    """"""


class IProvideGameSessions(Protocol):
    @abstractmethod
    def get(self) -> IGameSession:
        """"""


class NullGameSession(IGameSession):
    def start(self) -> None:
        raise NullGameSessionError()

    def wait_for_completion(self) -> None:
        raise NullGameSessionError()

    def stop(self) -> None:
        raise NullGameSessionError()


class NullGameSessionError(Exception):
    pass
