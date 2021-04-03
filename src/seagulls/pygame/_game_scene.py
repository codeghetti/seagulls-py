from abc import ABC

from ._overwrites import Surface


class GameScene(ABC):
    def start(self) -> None:
        pass

    def update(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        pass
