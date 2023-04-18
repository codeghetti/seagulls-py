import logging
import os
from functools import lru_cache
from multiprocessing.connection import Connection

import pygame
from pygame import SRCALPHA, Surface

from seagulls.cat_demos.engine.v2.components._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.components._size import Size

logger = logging.getLogger(__name__)


class WindowClient:

    def open(self) -> None:
        pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Cats!?")
        pygame.mouse.set_visible(False)
        pygame.font.init()

    def get_surface(self) -> Surface:
        return pygame.display.get_surface()

    def commit(self) -> None:
        pygame.display.flip()

    def close(self) -> None:
        pygame.display.quit()


class ServerWindowClient:

    _connection: ServiceProvider[Connection]

    def __init__(self, connection: ServiceProvider[Connection]) -> None:
        self._connection = connection

    def open(self) -> None:
        os.putenv("SDL_VIDEODRIVER", "dummy")
        pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Cats!?")
        pygame.mouse.set_visible(False)
        pygame.font.init()

    def commit(self) -> None:
        self._connection().send(pygame.surfarray.array3d(self.get_surface()))
        self.get_surface.cache_clear()

    @lru_cache()  # how can we use frame containers instead?
    def get_surface(self) -> Surface:
        return Surface(Size(width=800, height=800), flags=SRCALPHA, depth=32)

    def close(self) -> None:
        pass
