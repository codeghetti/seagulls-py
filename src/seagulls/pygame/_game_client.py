import logging
from abc import ABC

import pygame
from pygame import Surface

logger = logging.getLogger(__name__)


class GameScene(ABC):
    def render(self, surface: Surface) -> None:
        pass


class PygameWindowManager:

    _screen: Surface

    def __init__(self, screen: Surface):
        self._screen = screen
        pygame.init()

    def set_title(self, title: str) -> None:
        pygame.display.set_caption(title)

    def render_scene(self, scene: GameScene) -> None:
        scene.render(self._screen)
        pygame.display.flip()

    def close(self) -> None:
        pygame.display.quit()


class PygameClient:

    def open(self, width: int, height: int) -> PygameWindowManager:
        pygame.init()
        return PygameWindowManager(pygame.display.set_mode((width, height)))
