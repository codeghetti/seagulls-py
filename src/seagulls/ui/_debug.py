import logging
from pathlib import Path

from pygame.font import Font
from seagulls.pygame import GameControls, GameClock, Surface, GameObject, GameSceneObjects, \
    GameSceneManager

logger = logging.getLogger(__name__)


class DebugHud(GameObject):
    """
    UI Component to display FPS and other debug information during gameplay.
    """

    _scene_manager: GameSceneManager
    _clock: GameClock
    _controls: GameControls

    _background: Surface
    _active: bool

    def __init__(
            self,
            scene_manager: GameSceneManager,
            clock: GameClock,
            controls: GameControls):
        self.scene_manager = scene_manager
        self._clock = clock
        self._controls = controls

        self._background = Surface((1024, 20))
        self._background.fill((100, 100, 100))
        self._background.set_alpha(100)
        self._font = Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 14)
        self._active = False

    def update(self) -> None:
        if self._controls.should_toggle_debug_hud():
            self._active = not self._active
            logger.info(f"toggling debug hud: {self._active}")

    def render(self, surface: Surface) -> None:
        if not self._active:
            return

        fps = str(int(self._clock.get_fps())).rjust(3, " ")
        time = self._clock.get_time()
        num_objects = self.scene_manager.get_scene_objects().count_objects()
        img = self._font.render(
            f"FPS: {fps} | MS: {time} | OBJECTS: {num_objects}",
            True,
            (20, 20, 20)
        )
        text_height = img.get_height()
        padding = (self._background.get_height() - text_height) / 2

        surface.blit(self._background, (0, 0))
        surface.blit(img, (10, padding))

    def is_destroyed(self) -> bool:
        return False
