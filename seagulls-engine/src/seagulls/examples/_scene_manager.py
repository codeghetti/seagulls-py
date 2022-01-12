from seagulls.engine import IGameScene, IProvideGameScenes

from ._main_menu_scene import MainMenuScene


class ExampleSceneManager(IProvideGameScenes):
    _scene: MainMenuScene

    def __init__(self, scene: MainMenuScene):
        self._scene = scene

    def get_scene(self) -> IGameScene:
        return self._scene
