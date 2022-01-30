from functools import lru_cache

import pygame

from seagulls.assets import AssetManager
from seagulls.engine import GameObject, Surface


class SimpleStarsBackground(GameObject):

    _asset_manager: AssetManager

    def __init__(self, asset_manager: AssetManager):
        self._asset_manager = asset_manager

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        background = self._get_cached_background()
        surface.blit(background, (0, 0))

    @lru_cache()
    def _get_cached_background(self) -> Surface:
        sprite = self._asset_manager.load_sprite("environment/environment-stars").copy()

        sprite = pygame.transform.scale(
            sprite,
            (self._get_display_width(), self._get_display_height()))

        return sprite

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h
