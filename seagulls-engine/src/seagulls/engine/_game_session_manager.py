from abc import ABC, abstractmethod

from ._game_session import IGameSession


class IProvideGameSessions(ABC):

    @abstractmethod
    def get_session(self, scene: str) -> IGameSession:
        pass
