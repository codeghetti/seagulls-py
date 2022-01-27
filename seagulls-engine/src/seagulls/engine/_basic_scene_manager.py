from ._game_scene import IGameScene
from ._game_scene_manager import IProvideGameScenes


class BasicSceneManager(IProvideGameScenes):
    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get_scene(self) -> IGameScene:
        return self._scene
