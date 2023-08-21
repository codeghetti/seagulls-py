from seagulls.session import (
    IGameSession,
    IProvideGameSessions,
)


class RpgSessionProvider(IProvideGameSessions):
    _session: IGameSession

    def __init__(self, session: IGameSession):
        self._session = session

    def set(self, session: IGameSession) -> None:
        self._session = session

    def get(self) -> IGameSession:
        return self._session
