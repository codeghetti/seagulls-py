from typing import Tuple, Iterable

from ._executables import IExecutable


class GameSessionStages:

    _stages: Tuple[IExecutable, ...]

    def __init__(self, stages: Tuple[IExecutable, ...]) -> None:
        self._stages = stages

    def stages(self) -> Iterable[IExecutable]:
        return self._stages


class GameSession:

    _session_stages: GameSessionStages

    def __init__(self, session_stages: GameSessionStages) -> None:
        self._session_stages = session_stages

    def run(self) -> None:
        for stage in self._session_stages.stages():
            stage.execute()
