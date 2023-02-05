from typing import Tuple, Iterable

from seagulls.cat_demos.engine.v2._executables import IExecutable, executable
from seagulls.cat_demos.engine.v2._service_provider import ServiceProvider, provider


class GameSessionStages:

    _stages: Tuple[ServiceProvider[IExecutable], ...]

    def __init__(self, stages: Tuple[ServiceProvider[IExecutable], ...]) -> None:
        self._stages = stages

    def stages(self) -> Iterable[IExecutable]:
        for stage in self._stages:
            yield stage.get_service()


class GameSession:

    _session_stages: GameSessionStages

    def __init__(self, session_stages: GameSessionStages) -> None:
        self._session_stages = session_stages

    def run(self) -> None:
        for stage in self._session_stages.stages():
            stage.execute()


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


if __name__ == "__main__":
    container = Container()
    client = container.game_client()
    session = client.get_session()
    session.run()
