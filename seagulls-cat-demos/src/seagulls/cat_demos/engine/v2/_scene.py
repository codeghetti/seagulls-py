from abc import abstractmethod
from typing import Protocol

from seagulls.cat_demos.engine.v2.components._scene_objects import GameObjectId


class ITick(Protocol):

    @abstractmethod
    def tick(self) -> None:
        pass


class IUpdate(Protocol):
    @abstractmethod
    def update(self, game_object: GameObjectId) -> None:
        pass
