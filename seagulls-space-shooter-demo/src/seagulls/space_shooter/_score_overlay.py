from functools import lru_cache
from pathlib import Path

from pygame.font import Font
from seagulls.engine import GameObject, Surface

from ._fit_to_screen import FitToScreen
from ._score_tracker import ScoreTracker


class ScoreOverlay(GameObject):
    _position_buffer = 100
    _fit_to_screen: FitToScreen

    def __init__(
            self,
            score_tracker: ScoreTracker,
            fit_to_screen: FitToScreen):

        self._score_tracker = score_tracker
        self._fit_to_screen = fit_to_screen

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
                self._fit_to_screen.get_x_boundaries().y - self._position_buffer,
                self._fit_to_screen.get_y_boundaries().y - 30
            ))

    def reset(self) -> None:
        self._score_tracker.reset()

    @lru_cache()
    def _font(self) -> Font:
        return Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 18)
