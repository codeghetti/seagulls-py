import logging
import os
import pygame
from abc import abstractmethod
from functools import lru_cache
from multiprocessing.connection import Connection
from pygame import SRCALPHA, Surface
from typing import Iterable, NamedTuple, Protocol

from seagulls.cat_demos.engine.v2.components._component_containers import (
    ObjectDataId
)
from seagulls.cat_demos.engine.v2.components._service_provider import (
    ServiceProvider
)
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEvent,
    GameEventId
)
from seagulls.cat_demos.engine.v2.position._point import Position

logger = logging.getLogger(__name__)


class SurfaceBytes(NamedTuple):
    bytes: bytes
    size: Size


class IWindow(Protocol):
    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def get_layer(self, name: str) -> Surface:
        pass

    @abstractmethod
    def get_surface(self) -> Surface:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class WindowClient(IWindow):

    _layers: Iterable[str]

    def __init__(self, layers: Iterable[str]) -> None:
        self._layers = layers

    def open(self) -> None:
        pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Cats!?")
        pygame.mouse.set_visible(False)
        pygame.font.init()

    def commit(self) -> None:
        window_surface = pygame.display.get_surface()

        window_surface.blit(self.get_surface(), Position(x=0, y=0))
        for layer in self._layers:
            s = self.get_layer(layer)
            window_surface.blit(s, Position(x=0, y=0))

        pygame.display.flip()
        self._make_surface.cache_clear()

    def get_layer(self, name: str) -> Surface:
        if name not in self._layers:
            raise RuntimeError(f"layer not found: {name}")

        return self._make_surface(name)

    def get_surface(self) -> Surface:
        return self._make_surface("_default")

    def close(self) -> None:
        pygame.display.quit()

    @lru_cache()
    def _make_surface(self, name: str) -> Surface:
        return Surface(Size(width=800, height=800), flags=SRCALPHA, depth=32).copy()


class ServerWindowClient(IWindow):

    _layers: Iterable[str]
    _connection: ServiceProvider[Connection]

    def __init__(self, layers: Iterable[str], connection: ServiceProvider[Connection]) -> None:
        self._layers = layers
        self._connection = connection

    def get_layer(self, name: str) -> Surface:
        if name not in self._layers:
            raise RuntimeError(f"layer not found: {name}")

        return self._make_surface(name)

    def open(self) -> None:
        os.putenv("SDL_VIDEODRIVER", "dummy")
        pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Cats!?")
        pygame.mouse.set_visible(False)
        pygame.font.init()

    def commit(self) -> None:
        window_surface = self._make_surface("_window")

        window_surface.blit(self.get_surface(), Position(x=0, y=0))
        for layer in self._layers:
            s = self.get_layer(layer)
            window_surface.blit(s, Position(x=0, y=0))

        surface_bytes = pygame.image.tobytes(window_surface, "RGBA")
        event = GameEvent(
            id=SeagullsWindows.SURFACE_BYTES_EVENT,
            payload=SurfaceBytes(surface_bytes, Size(*window_surface.get_size())),
        )
        self._connection().send(event)
        self._make_surface.cache_clear()

    def get_surface(self) -> Surface:
        return self._make_surface("_default")

    def close(self) -> None:
        pass

    @lru_cache()
    def _make_surface(self, name: str) -> Surface:
        return Surface(Size(width=800, height=800), flags=SRCALPHA, depth=32).copy()


class SeagullsWindows:
    WINDOW_CLIENT_COMPONENT = ObjectDataId[WindowClient]("window-client")
    # TODO: is this supposed to also be called window-client so the dev can choose which to
    #       initialize? or do they both exist in every app and the dev chooses which one to pass
    #       into methods?
    SERVER_WINDOW_CLIENT_COMPONENT = ObjectDataId[WindowClient](
        "server-window-client"
    )
    SURFACE_BYTES_EVENT = GameEventId[SurfaceBytes]("window.surface-bytes")
