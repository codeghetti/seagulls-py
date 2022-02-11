from functools import lru_cache

import pygame
from pygame.font import Font
from seagulls.assets import AssetManager
from seagulls.engine import GameObject, Surface

from ._fit_to_screen import FitToScreen


class GameOverOverlay(GameObject):

    _asset_manager: AssetManager
    _fit_to_screen: FitToScreen

    def __init__(self, asset_manager: AssetManager, fit_to_screen: FitToScreen):
        self._asset_manager = asset_manager
        self._fit_to_screen = fit_to_screen

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        img = self._get_font().render(
            "GAME OVER",
            True,
            "red", "black"
        )
        img = pygame.transform.scale(
            img,
            (self._fit_to_screen.get_actual_surface_width() * img.get_width() / 1920,
             self._fit_to_screen.get_actual_surface_height() * img.get_height() / 1080
             ))
        surface.blit(img, (self._get_display_width() / 2 - 80, self._get_display_height() / 2))

    @lru_cache()
    def _get_font(self) -> Font:
        return Font(self._asset_manager.get_path("fonts/ubuntu-mono-v10-latin-regular.ttf"), 50)

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h
