from seagulls.engine import IGameSession
from seagulls.engine import IProvideGameSessions
from ._game_session import AsyncGameSession


class AsyncGameSessionManager(IProvideGameSessions):
    def get_session(self, scene: str) -> IGameSession:
        return AsyncGameSession(name=scene)
