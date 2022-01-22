from seagulls.engine import IGameScene, IProvideGameScenes


class ExampleSceneManager(IProvideGameScenes):
    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get_scene(self) -> IGameScene:
        return self._scene
