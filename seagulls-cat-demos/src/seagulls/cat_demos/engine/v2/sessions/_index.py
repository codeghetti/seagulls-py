import logging

from seagulls.cat_demos.engine.v2.components._entities import GameSceneId
from seagulls.cat_demos.engine.v2.scenes._client import SceneEvents
from ._executables import IExecutable

logger = logging.getLogger(__name__)


class OpenIndexScene(IExecutable):
    def __call__(self) -> None:
        scene_id = GameSceneId("index")
        logger.warning(f"scene loaded: {scene_id}")
        logger.warning(f"available event: {SceneEvents.open_scene(scene_id)}")
        logger.warning(f"available event: {SceneEvents.execute_scene(scene_id)}")
        logger.warning(f"available event: {SceneEvents.close_scene(scene_id)}")


class CloseIndexScene(IExecutable):

    def __call__(self) -> None:
        print("Goodbye!")
