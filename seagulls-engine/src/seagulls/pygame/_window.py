from functools import cache
from typing import Optional

import pygame
from pygame import Surface

from seagulls.rendering import SizeDict

from ._surface import IProvideSurfaces


class WindowSurface(IProvideSurfaces):

    _current_surface: Optional[Surface]
    # Is it bad to depend on a data structure like this instead of using Size?
    _resolution_setting: SizeDict

    def __init__(self, resolution_setting: SizeDict):
        self._resolution_setting = resolution_setting
        self._current_surface = None

    def initialize(self) -> None:
        self._current_surface = self._get_window()

    def update_window(self) -> None:
        if self._current_surface is None:
            raise RuntimeError("Window must be initialized with WindowSurface.initialize()")
        self._current_surface = self._get_window()

    def get(self) -> Surface:
        if self._current_surface is None:
            raise RuntimeError("Window must be initialized with WindowSurface.initialize()")
        return self._current_surface

    def set_resolution(self, resolution: SizeDict) -> None:
        self._resolution_setting = resolution

    def _get_window(self) -> Surface:
        surface = pygame.display.set_mode(
            (self._resolution_setting["height"], self._resolution_setting["width"])
        )

        # Adding some backgrounds to debug with for now
        surface.fill((200, 20, 20))

        inner = Surface(
            (self._resolution_setting["height"] - 10, self._resolution_setting["width"] - 10))
        inner.fill((20, 200, 20))

        surface.blit(inner, (5, 5))

        return surface
