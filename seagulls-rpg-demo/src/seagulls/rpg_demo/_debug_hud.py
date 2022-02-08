"""
This module contains classes for rendering a Debug Hud in game scenes.
"""
import logging
from functools import lru_cache
from pathlib import Path

from pygame import font
from pygame.font import Font

from seagulls.assets import AssetManager
from seagulls.engine import GameClock, GameObject, Surface

logger = logging.getLogger(__name__)


class DebugHud(GameObject):
    """
    UI Component to display FPS and other debug information during gameplay.
    """

    _asset_manager: AssetManager
    _game_clock: GameClock

    def __init__(self, asset_manager: AssetManager, game_clock: GameClock):
        """
        Initializes a Debug Hud where `game_clock` controls how we measure time.
        """
        self._asset_manager = asset_manager
        self._game_clock = game_clock
        self._background = Surface((1024, 20))
        self._background.fill((100, 100, 100))
        self._background.set_alpha(100)

    def tick(self) -> None:
        """
        Does nothing because Debug Huds do not need to perform any logic on tick().
        """
        pass

    def render(self, surface: Surface) -> None:
        """
        Renders the debug information onto the passed in Surface object.
        """
        fps = str(int(self._game_clock.get_fps())).rjust(3, " ")
        time = self._game_clock.get_time()
        img = self._font().render(
            f"FPS: {fps} | MS: {time}",
            True,
            (20, 20, 20)
        )
        text_height = img.get_height()
        padding = (self._background.get_height() - text_height) / 2

        surface.blit(self._background, (0, 0))
        surface.blit(img, (10, padding))

    @lru_cache()
    def _font(self) -> Font:
        font.init()
        return Font(
            self._asset_manager.get_path("fonts/ubuntu-mono-v10-latin-regular.ttf"), 14)
