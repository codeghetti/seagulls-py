from functools import lru_cache
from pathlib import Path

import pygame
from pygame.font import Font
from seagulls.engine import GameObject, Surface

from ._score_tracker import ScoreTracker


class ScoreOverlay(GameObject):
    _position_buffer = 200

    def __init__(
            self,
            score_tracker: ScoreTracker):

        self._score_tracker = score_tracker

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        img = self._font().render(
            f"Score: {self._score_tracker.get_score()}",
            True,
            "red", "black"
        )
        surface.blit(
            img,
            (
                self._get_display_width() - self._position_buffer,
                self._get_display_height() - 100
            ))

    def reset(self) -> None:
        self._score_tracker.reset()

    @lru_cache()
    def _font(self) -> Font:
        return Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 18)

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h
