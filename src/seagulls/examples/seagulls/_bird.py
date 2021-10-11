import logging
from functools import lru_cache

import pygame
from pygame.transform import flip

from seagulls.assets import AssetManager
from seagulls.engine import (
    GameClock,
    GameControls,
    GameObject,
    Rect,
    Surface,
    Vector2
)

logger = logging.getLogger(__name__)


class Bird(GameObject):

    _clock: GameClock
    _asset_manager: AssetManager
    _game_controls: GameControls
    _size: Vector2
    _position: Vector2
    _velocity: Vector2

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager,
            game_controls: GameControls):
        self._clock = clock
        self._asset_manager = asset_manager
        self._game_controls = game_controls

        self._size = Vector2(64, 64)
        # This is the starting position for new wizards
        self._position = Vector2(500, 40)
        self._velocity = Vector2(0, 0)

    def tick(self) -> None:
        if self._game_controls.should_fire():
            logger.info("POOPING")

        if self._game_controls.is_left_moving():
            logger.info("MOVE LEFT")
            self._velocity = Vector2(-1, 0)
        elif self._game_controls.is_right_moving():
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

        if self._game_controls.is_left_moving():
            sprite = flip(sprite, True, False)

        surface.blit(sprite, (blit_position.x, blit_position.y))

    def _get_sprite(self) -> Surface:
        sprite_sheet = self._get_sprite_sheet()
        rect = Rect((64 * 0, 0), (64, 64))

        result = Surface(rect.size)
        result.blit(sprite_sheet, (0, 0), rect)

        # Not really sure why this is needed but meh. Losing transparency if I don't do this.
        colorkey = result.get_at((0, 0))
        result.set_colorkey(colorkey, pygame.RLEACCEL)

        return flip(result.convert_alpha(), True, False)

    @lru_cache()
    def _get_sprite_sheet(self) -> Surface:
        return self._asset_manager.load_sprite("seagull/seagull-walking")
