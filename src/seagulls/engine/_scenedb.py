from abc import ABC, abstractmethod
from ._game_scene import GameScene


class ILocateScenes(ABC):

    @abstractmethod
    def get_by_id(self, scene_id: str) -> GameScene:
        pass


class ScenesClient:
    _locator: ILocateScenes

    def find_by_id(self, scene_id: str) -> GameScene:
        return self._locator.get_by_id(scene_id)
