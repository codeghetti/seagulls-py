from abc import ABC, abstractmethod
from typing import Callable, List

from ._pyagme import Surface


class GameObject(ABC):

    @abstractmethod
    def tick(self) -> None:
        pass

    @abstractmethod
    def render(self, surface: Surface) -> None:
        pass


class GameObjectsCollection:
    _game_objects: List[GameObject]

    def __init__(self) -> None:
        self._game_objects = []

    def add(self, game_object: GameObject) -> None:
        self._game_objects.append(game_object)

    def apply(self, func: Callable[[GameObject], None]) -> None:
        for game_object in self._game_objects:
            func(game_object)
