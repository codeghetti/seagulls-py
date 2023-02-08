from ._executables import IExecutable, executable
from ._service_provider import ServiceProvider, provider
from ._game_session import GameSession, GameSessionStages
from ._session_stages import GameStages


class GameClient:

    _session: ServiceProvider[GameSession]

    def __init__(self, session: ServiceProvider[GameSession]) -> None:
        self._session = session

    def get_session(self) -> GameSession:
        return self._session.get_service()


class Container:

    def game_client(self) -> GameClient:
        return GameClient(session=provider(self._game_session))

    def _game_session(self) -> GameSession:
        return GameSession(session_stages=self._session_stages())

    def _session_stages(self) -> GameSessionStages:
        return GameSessionStages(tuple([
            provider(self._open_session),
            provider(self._run_session),
            provider(self._close_session),
        ]))

    def _open_session(self) -> IExecutable:
        return executable(lambda: print("default executable: init session"))

    def _run_session(self) -> IExecutable:
        return executable(lambda: print("default executable: run session"))

    def _close_session(self) -> IExecutable:
        return executable(lambda: print("default executable: close session"))

    def _game_stages(self) -> GameStages:
        return GameStages()
