from functools import lru_cache
from typing import Tuple

import pygame
from seagulls.engine import Vector2


class FitToScreen:

    @lru_cache()
    def get_x_boundaries(self) -> Tuple[float, float]:
        return (
            self.get_x_padding(),
            self.get_x_padding() + self.get_actual_surface_width()
        )

    @lru_cache()
    def get_y_boundaries(self) -> Tuple[float, float]:
        return (
            self.get_y_padding(),
            self.get_y_padding() + self.get_actual_surface_height()
        )

    @lru_cache()
    def get_x_padding(self) -> float:
        return (self._get_current_window_width() - self.get_actual_surface_width()) / 2

    @lru_cache()
    def get_y_padding(self) -> float:
        return (self._get_current_window_height() - self.get_actual_surface_height()) / 2

    @lru_cache()
    def get_actual_surface_width(self) -> float:
        if self._is_too_wide():
            actual_width = self.get_actual_surface_height() * 1.6
        else:
            actual_width = self._get_current_window_width()

        return actual_width

    @lru_cache()
    def get_actual_surface_height(self) -> float:
        if self._is_too_thin():
            actual_height = self._get_current_window_width() / 1.6
        else:
            actual_height = self._get_current_window_height()

        return actual_height

    @lru_cache()
    def _is_too_wide(self) -> bool:
        return self._get_current_aspect_ratio() > 1.6

    @lru_cache()
    def _is_too_thin(self) -> bool:
        return self._get_current_aspect_ratio() < 1.6

    @lru_cache()
    def _is_ideal_aspect_ratio(self) -> bool:
        # aspect ratio should be 16:10
        return self._get_current_aspect_ratio() == 1.6

    @lru_cache()
    def _get_current_aspect_ratio(self) -> float:
        return self._get_current_window_width() / self._get_current_window_height()

    @lru_cache()
    def _get_current_window_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_current_window_height(self) -> int:
        return pygame.display.Info().current_h
