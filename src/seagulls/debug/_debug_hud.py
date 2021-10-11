import logging
from pathlib import Path

from pygame.font import Font

from seagulls.engine import GameClock, GameObject, Surface

logger = logging.getLogger(__name__)


class DebugHud(GameObject):
    """
    UI Component to display FPS and other debug information during gameplay.
    """

    _game_clock: GameClock

    def __init__(self, game_clock: GameClock):
        self._game_clock = game_clock
        self._background = Surface((1024, 20))
        self._background.fill((100, 100, 100))
        self._background.set_alpha(100)
        self._font = Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 14)

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        fps = str(int(self._game_clock.get_fps())).rjust(3, " ")
        time = self._game_clock.get_time()
        img = self._font.render(
            f"FPS: {fps} | MS: {time}",
            True,
            (20, 20, 20)
        )
        text_height = img.get_height()
        padding = (self._background.get_height() - text_height) / 2

        surface.blit(self._background, (0, 0))
        surface.blit(img, (10, padding))
