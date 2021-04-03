import logging

import pygame
from pygame import Surface
from ._game_scene import GameScene

logger = logging.getLogger(__name__)


class GameWindow:

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


class GameWindowFactory:

    _created: bool

    def __init__(self):
        self._created = False

    def create(self, width: int, height: int) -> GameWindow:
        if self._created:
            raise RuntimeError("Multiple game windows are not yet supported")

        self._created = True
        return GameWindow(pygame.display.set_mode((width, height)))
