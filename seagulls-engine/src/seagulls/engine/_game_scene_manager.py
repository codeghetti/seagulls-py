from abc import ABC, abstractmethod

from ._game_scene import IGameScene


class IProvideGameScenes(ABC):

    @abstractmethod
    def get_scene(self) -> IGameScene:
        pass
