import logging
import os
from functools import lru_cache
from multiprocessing.connection import Connection
from typing import NamedTuple

import pygame
from pygame import SRCALPHA, Surface

from seagulls.cat_demos.engine.v2.components._component_containers import (
    GameComponentId
)
from seagulls.cat_demos.engine.v2.components._service_provider import (
    ServiceProvider
)
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEvent,
    GameEventId
)

logger = logging.getLogger(__name__)


class SurfaceBytes(NamedTuple):
    bytes: bytes
    size: Size


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
        surface = self.get_surface()
        surface_bytes = pygame.image.tobytes(surface, "RGBA")
        event = GameEvent(
            id=SeagullsWindows.SURFACE_BYTES_EVENT,
            payload=SurfaceBytes(surface_bytes, Size(*surface.get_size())),
        )
        self._connection().send(event)
        self.get_surface.cache_clear()

    @lru_cache()  # how can we use frame containers instead?
    def get_surface(self) -> Surface:
        return Surface(Size(width=800, height=800), flags=SRCALPHA, depth=32)

    def close(self) -> None:
        pass


class SeagullsWindows:
    WINDOW_CLIENT_COMPONENT = GameComponentId[WindowClient]("window-client")
    # TODO: is this supposed to also be called window-client so the dev can choose which to
    #       initialize? or do they both exist in every app and the dev chooses which one to pass
    #       into methods?
    SERVER_WINDOW_CLIENT_COMPONENT = GameComponentId[WindowClient](
        "server-window-client"
    )
    SURFACE_BYTES_EVENT = GameEventId[SurfaceBytes]("window.surface-bytes")
