from seagulls.session import (
    IGameSession,
    IProvideGameSessions,
    IStopGameSessions
)


class MySessionStopper(IStopGameSessions):

    _session: IStopGameSessions

    def __init__(self, session: IStopGameSessions):
        self._session = session

    def wait_for_completion(self) -> None:
        raise RuntimeError("Can't wait for completion?")

    def stop(self) -> None:
        self._session.stop()


class RpgSessionProvider(IProvideGameSessions):
    _session: IGameSession

    def __init__(self, session: IGameSession):
        self._session = session

    def set(self, session: IGameSession) -> None:
        self._session = session

    def get(self) -> IGameSession:
        return self._session
