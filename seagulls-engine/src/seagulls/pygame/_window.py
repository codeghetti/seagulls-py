import logging
from typing import Optional, Tuple

import pygame
from pygame import Surface

from seagulls.rendering import SizeDict

from ._surface import IProvideSurfaces

logger = logging.getLogger(__name__)


class WindowSurface(IProvideSurfaces):

    _current_surface: Optional[Surface]
    # Is it bad to depend on a data structure like this instead of using Size?
    _resolution_setting: SizeDict
    _camera_setting: SizeDict
    _padding_color = Tuple[int, int, int]

    def __init__(self, resolution_setting: SizeDict, camera_setting: SizeDict):
        self._resolution_setting = resolution_setting
        self._camera_setting = camera_setting
        self._padding_color = tuple([100, 100, 100])
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
        return self._current_surface.copy()

    def update(self, surface: Surface):
        if self._current_surface is None:
            raise RuntimeError("Window must be initialized with WindowSurface.initialize()")

        window_height = self._resolution_setting["height"]
        window_width = self._resolution_setting["width"]

        camera_height = self._camera_setting["height"]
        camera_width = self._camera_setting["width"]

        window_aspect_ratio = window_height / window_width
        camera_aspect_ratio = camera_height / camera_width

        if camera_aspect_ratio > window_aspect_ratio:
            # Need to add black padding on the left/right until ratios match, then resize
            needed_width = camera_height / window_aspect_ratio
            # Total of padding
            empty_space = abs(needed_width - camera_width)
            # We make a fully filled in surface matching the padding color
            final_surface = Surface((needed_width, camera_height))
            final_surface.fill(self._padding_color)
            # And then print the camera image in the middle
            final_surface.blit(surface, (empty_space / 2, 0))
        elif camera_aspect_ratio < window_aspect_ratio:
            # Need to add black padding on the top/bottom until ratios match, then resize
            needed_height = camera_width * window_aspect_ratio
            # Total of padding
            empty_space = needed_height - camera_height
            # We make a fully filled in surface matching the padding color
            final_surface = Surface((camera_width, needed_height))
            final_surface.fill(self._padding_color)
            # And then print the camera image in the middle
            final_surface.blit(surface, (0, empty_space / 2))
        else:
            # No padding needed
            final_surface = surface
            pass

        scaled_surface = pygame.transform.scale(final_surface, (window_width, window_height))
        self._current_surface.blit(source=scaled_surface, dest=(0, 0))

        pygame.display.flip()

    def set_resolution(self, resolution: SizeDict) -> None:
        self._resolution_setting = resolution

    def _get_window(self) -> Surface:
        surface = pygame.display.set_mode(
            (self._resolution_setting["width"], self._resolution_setting["height"])
        )
        # TODO where does window caption logic go?
        pygame.display.set_caption("Our Game")

        surface.fill(self._padding_color)

        return surface
