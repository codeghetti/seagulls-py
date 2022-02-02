from functools import lru_cache

import pygame

from ._pygame import Surface


class SurfaceRenderer:
    def start(self) -> None:
        self._get_surface()

    def render(self, surface: Surface) -> None:
        self._get_surface().blit(surface, (0, 0))
        pygame.display.flip()

    @lru_cache()
    def _get_surface(self) -> Surface:
        return pygame.display.set_mode((2200, 700))
