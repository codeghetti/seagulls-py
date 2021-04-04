import logging
from functools import lru_cache
from typing import List

import pygame
from seagulls.assets import AssetManager
from seagulls.pygame import (
    GameTimeProvider,
    Vector2,
    Surface, GameControls, Rect,
)

logger = logging.getLogger(__name__)


class SimpleWizard:

    _clock: GameTimeProvider
    _asset_manager: AssetManager
    _sprite: Surface
    _controls: GameControls

    _size: Vector2
    _position: Vector2
    _velocity: Vector2
    _current_walking_frame: float

    def __init__(
            self, clock: GameTimeProvider, asset_manager: AssetManager, controls: GameControls):
        self._clock = clock
        self._asset_manager = asset_manager
        self._controls = controls

        self._size = Vector2(64, 64)
        # This is the starting position for new wizards
        self._position = Vector2(0, 518)
        self._velocity = Vector2(1, 0)
        self._current_walking_frame = 0.0

    def update(self) -> None:
        # A bit hacky but we flip the direction the wizard is moving
        # When ever they get close to the edges of the screen
        if self._position.x > 1015:
            self._velocity = Vector2(-1, 0)
        elif self._position.x < 10:
            self._velocity = Vector2(1, 0)

        if self._controls.should_fire():
            logger.info("FIRING!")

        delta = self._clock.get_time()

        self._position = self._position + (self._velocity * delta / 10)

    def render(self, surface: Surface) -> None:
        sprite = self._get_sprite().copy().convert_alpha()
        radius = self._size.x / 2
        blit_position = self._position - Vector2(radius)
        surface.blit(sprite, (blit_position.x, blit_position.y))

    def _get_sprite(self) -> Surface:
        self._current_walking_frame += self._clock.get_time() / 300
        if int(self._current_walking_frame) >= len(self._walking_frames()):
            self._current_walking_frame = 0

        return self._walking_frames()[int(self._current_walking_frame)]

    @lru_cache()
    def _walking_frames(self) -> List[Surface]:
        return [
            self._sprite_sheet_slice(Rect((0, 0), (64, 64))),
            self._sprite_sheet_slice(Rect((64, 0), (64, 64))),
        ]

    def _sprite_sheet_slice(self, rect: Rect) -> Surface:
        sprite_sheet = self._get_sprite_sheet()

        result = Surface(rect.size)
        result.blit(sprite_sheet, (0, 0), rect)

        # Not really sure why this is needed but meh. Losing transparency if I don't do this.
        colorkey = result.get_at((0, 0))
        result.set_colorkey(colorkey, pygame.RLEACCEL)

        return result.convert_alpha()

    @lru_cache()
    def _get_sprite_sheet(self) -> Surface:
        return self._asset_manager.load_sprite("wizard/wizard1-spritesheet")


class SimpleWizardFactory:
    _asset_manager: AssetManager
    _clock: GameTimeProvider
    _controls: GameControls

    def __init__(
            self,
            asset_manager: AssetManager,
            clock: GameTimeProvider,
            controls: GameControls):
        self._asset_manager = asset_manager
        self._clock = clock
        self._controls = controls

    def create(self) -> SimpleWizard:
        return SimpleWizard(
            clock=self._clock,
            asset_manager=self._asset_manager,
            controls=self._controls,
        )
