from abc import ABC, abstractmethod
from typing import List, Tuple

from ._game_object import GameObject

from ._overwrites import Surface


class GameSceneObjects:
    _objects: List[GameObject]

    def __init__(self):
        self._objects = []

    def add(self, obj: GameObject) -> None:
        self._objects.append(obj)

    def get_objects(self) -> Tuple[GameObject, ...]:
        return tuple(self._objects)


class GameScene(ABC):

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self, surface: Surface) -> None:
        pass

    @abstractmethod
    def add_game_object(self, obj: GameObject) -> None:
        pass
