from abc import ABC

from pygame import Surface


class GameScene(ABC):
    def render(self, surface: Surface) -> None:
        pass
