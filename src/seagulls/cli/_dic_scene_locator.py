from seagulls.engine import ILocateScenes, GameScene
from ._di_container import SeagullsDiContainer


class DiCSceneLocator(ILocateScenes):

    _di_container: SeagullsDiContainer

    def get_by_id(self, scene_id: str) -> GameScene:
        return self._di_container.__getattr__(f"scene_{scene_id}")()
