from functools import lru_cache
from pathlib import Path

import pygame
from pygame.font import Font
from seagulls.engine import GameObject, Surface


class GameOverOverlay(GameObject):

    _font: Font

    def __init__(self):
        self._font = Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 50)

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        img = self._font.render(
            "GAME OVER",
            True,
            "red", "black"
        )
        surface.blit(img, (self._get_display_width() / 2 - 80, self._get_display_height() / 2))

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h
