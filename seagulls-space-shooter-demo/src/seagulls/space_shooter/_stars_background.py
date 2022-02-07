import logging
from functools import lru_cache

import pygame
from seagulls.assets import AssetManager
from seagulls.engine import GameObject, Surface

from ._fit_to_screen import FitToScreen

logger = logging.getLogger(__name__)


class SimpleStarsBackground(GameObject):

    _asset_manager: AssetManager
    _fit_to_screen: FitToScreen

    def __init__(
            self,
            asset_manager: AssetManager,
            fit_to_screen: FitToScreen):
        self._asset_manager = asset_manager
        self._fit_to_screen = fit_to_screen

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        background = self._get_cached_background()
        surface.blit(
            background,
            (self._fit_to_screen.get_x_padding(), self._fit_to_screen.get_y_padding()))

    @lru_cache()
    def _get_cached_background(self) -> Surface:
        sprite = self._asset_manager.load_sprite("environment/environment-stars").copy()
        sprite = pygame.transform.scale(
            sprite,
            (
                self._fit_to_screen.get_actual_surface_width(),
                self._fit_to_screen.get_actual_surface_height())
        )

        return sprite
