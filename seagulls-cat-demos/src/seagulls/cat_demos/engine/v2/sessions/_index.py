import logging

from ._executables import IExecutable
from ..scenes._scene_client import SceneContext

logger = logging.getLogger(__name__)


class OpenScene(IExecutable):

    _scene: SceneContext

    def __init__(self, scene: SceneContext) -> None:
        self._scene = scene

    def execute(self) -> None:
        print(f"scene opened: {self._scene.get()}")


class CloseScene(IExecutable):

    _scene: SceneContext

    def __init__(self, scene: SceneContext) -> None:
        self._scene = scene

    def execute(self) -> None:
        print(f"scene closed: {self._scene.get()}")
