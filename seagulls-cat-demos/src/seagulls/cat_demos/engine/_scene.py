from typing import Tuple, Iterable

from ._executables import IExecutable


class GameSceneStages:

    _stages: Tuple[IExecutable, ...]

    def __init__(self, stages: Tuple[IExecutable, ...]) -> None:
        self._stages = stages

    def stages(self) -> Iterable[IExecutable]:
        return self._stages


class GameScene:

    _scene_stages: GameSceneStages

    def __init__(self, scene_stages: GameSceneStages) -> None:
        self._scene_stages = scene_stages

    def run(self) -> None:
        for stage in self._scene_stages.stages():
            stage.execute()


"""
- session init
    - window open
    - scene load
- session run
    - scene init
    - scene run
        - input update
        - input events trigger
        - objects update
        - objects render
            - environment background render
            - characters render
            - environment foreground render
            - ui render
    - scene end
- session end
    - window close
"""
