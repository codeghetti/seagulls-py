from abc import ABC, abstractmethod
from typing import List, Tuple

from seagulls.engine import Vector2


class Collidable(ABC):

    @abstractmethod
    def check_collision(self, position: Vector2) -> bool:
        pass

    @abstractmethod
    def collide(self) -> None:
        pass


class CollidablesCollection:

    _collidables: List[Collidable]

    def __init__(self):
        self._collidables = []

    def add(self, item: Collidable) -> None:
        self._collidables.append(item)

    def get_collisions(self, position: Vector2) -> Tuple[Collidable, ...]:
        result = []
        for item in self._collidables:
            if item.check_collision(position):
                result.append(item)

        return tuple(result)
