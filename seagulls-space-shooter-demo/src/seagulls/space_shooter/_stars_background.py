import logging
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

        if self._is_ideal_aspect_ratio():
            surface.blit(background, (0, 0))
        elif self._is_too_thin():
            surface.blit(background, (0, self._get_y_padding()))
        else:
            surface.blit(background, (self._get_x_padding(), 0))

    @lru_cache()
    def _get_cached_background(self) -> Surface:
        sprite = self._asset_manager.load_sprite("environment/environment-stars").copy()

        if self._is_ideal_aspect_ratio():
            sprite = pygame.transform.scale(
                sprite,
                (self._get_display_width(), self._get_display_height()))
        elif self._is_too_thin():
            sprite = pygame.transform.scale(
                sprite,
                (self._get_display_width(),
                 self._get_display_width() / 1.6)
            )
        else:
            sprite = pygame.transform.scale(
                sprite,
                (self._get_display_width() * 1.6 / self._get_aspect_ratio(),
                 self._get_display_height())
            )

        return sprite

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h

    @lru_cache()
    def _get_aspect_ratio(self) -> float:
        return pygame.display.Info().current_w / pygame.display.Info().current_h

    def _is_ideal_aspect_ratio(self) -> bool:
        return self._get_aspect_ratio() == 1.6

    def _get_x_padding(self) -> float:
        actual_width = self._get_display_width() * 1.6 / self._get_aspect_ratio()
        return (self._get_display_width() - actual_width) / 2

    def _get_y_padding(self) -> float:
        actual_height = self._get_display_width() / 1.6
        return (self._get_display_height() - actual_height) / 2

    def _is_too_wide(self) -> bool:
        return self._get_aspect_ratio() > 1.6

    def _is_too_thin(self) -> bool:
        return self._get_aspect_ratio() < 1.6
