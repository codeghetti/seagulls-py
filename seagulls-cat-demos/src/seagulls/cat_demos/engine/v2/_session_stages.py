from typing import Iterable, Tuple

from ._executables import IExecutable
from seagulls.cat_demos.engine.v2._service_provider import ServiceProvider


class GameSessionStages:

    _stages: Tuple[ServiceProvider[IExecutable], ...]

    def __init__(self, stages: Tuple[ServiceProvider[IExecutable], ...]) -> None:
        self._stages = stages

    def stages(self) -> Iterable[IExecutable]:
        for stage in self._stages:
            yield stage.get_service()


class SceneStages:
    def open_scene(self) -> None:
        pass

    def run_scene(self) -> None:
        pass

    def close_scene(self) -> None:
        pass


class GameSceneStages:
    _scenes: Tuple[ServiceProvider[IExecutable], ...]

    def __init__(self, stages: Tuple[ServiceProvider[IExecutable], ...]) -> None:
        self._stages = stages

    def stages(self) -> Iterable[IExecutable]:
        for stage in self._stages:
            yield stage.get_service()


class GameStages:

    def open_session(self) -> None:
        print("default executable: init session")

    def run_session(self) -> None:
        print("default executable: run session")
        for scene in self._scene_provider.scenes():
            scene.open_scene()
            scene.run_scene()
            scene.close_scene()

    def close_session(self) -> None:
        print("default executable: close session")
