from seagulls.engine import IProvideGameScenes, IGameScene
from ._game_scene import SeagullGameScene


class SeagullsGameSceneManager(IProvideGameScenes):
    def get_scene(self, name: str) -> IGameScene:
        return SeagullGameScene(name=name)
