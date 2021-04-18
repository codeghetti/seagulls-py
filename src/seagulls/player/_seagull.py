import logging
from functools import lru_cache

import pygame
from seagulls.assets import AssetManager
from seagulls.engine import (
    GameObject,
    Surface,
    GameTimeProvider,
    GameSceneManager,
    Vector2,
    GameControls, Rect
)

logger = logging.getLogger(__name__)


class PlayerSeagull(GameObject):

    _controls: GameControls
    _clock: GameTimeProvider
    _scene_manager: GameSceneManager
    _asset_manager: AssetManager

    def __init__(
            self,
            controls: GameControls,
            clock: GameTimeProvider,
            scene_manager: GameSceneManager,
            asset_manager: AssetManager):
        self._controls = controls
        self._clock = clock
        self._scene_manager = scene_manager
        self._asset_manager = asset_manager

        self._size = Vector2(64, 64)
        # This is the starting position for new wizards
        self._position = Vector2(500, 40)
        self._velocity = Vector2(0, 0)

    def update(self) -> None:
        if self._controls.should_fire():
            logger.info("POOPING")

        if self._controls.is_left_moving():
            logger.info("MOVE LEFT")
            self._velocity = Vector2(-1, 0)
        elif self._controls.is_right_moving():
            logger.info("MOVE RIGHT")
            self._velocity = Vector2(1, 0)
        else:
            self._velocity = Vector2(0, 0)

        delta = self._clock.get_time()

        self._position = self._position + (self._velocity * delta / 10)

        if self._position.x < 30:
            self._position.x = 30

        if self._position.x > 995:
            self._position.x = 995

    def render(self, surface: Surface) -> None:
        sprite = self._get_sprite().copy().convert_alpha()
        radius = self._size.x / 2
        blit_position = self._position - Vector2(radius)
        surface.blit(sprite, (blit_position.x, blit_position.y))

    def _get_sprite(self) -> Surface:
        sprite_sheet = self._get_sprite_sheet()
        rect = Rect((64 * 0, 0), (64, 64))

        result = Surface(rect.size)
        result.blit(sprite_sheet, (0, 0), rect)

        # Not really sure why this is needed but meh. Losing transparency if I don't do this.
        colorkey = result.get_at((0, 0))
        result.set_colorkey(colorkey, pygame.RLEACCEL)

        return result.convert_alpha()

    @lru_cache()
    def _get_sprite_sheet(self) -> Surface:
        return self._asset_manager.load_sprite("seagull/seagull-walking")

    def is_destroyed(self) -> bool:
        return False
