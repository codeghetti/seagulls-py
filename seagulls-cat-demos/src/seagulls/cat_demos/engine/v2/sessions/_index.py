import logging

from seagulls.cat_demos.engine.v2.components._entities import GameSceneId

from ._executables import IExecutable

logger = logging.getLogger(__name__)


class OpenIndexScene(IExecutable):
    def __call__(self) -> None:
        scene_id = GameSceneId("index")
        logger.debug(f"scene loaded: {scene_id}")


class CloseIndexScene(IExecutable):
    def __call__(self) -> None:
        print("Goodbye!")
