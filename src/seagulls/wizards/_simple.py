import logging
from enum import Enum, auto
from functools import lru_cache
from random import random
from typing import List

import pygame
from seagulls.assets import AssetManager
from seagulls.attacks import WizardFireballFactory
from seagulls.engine import (
    GameTimeProvider,
    Vector2,
    Surface,
    Rect,
    GameObject,
    GameSceneManager,
)

logger = logging.getLogger(__name__)


class WizardState(Enum):
    STANDING = auto()
    WALKING = auto()
    ATTACKING = auto()


class SimpleWizard(GameObject):

    _clock: GameTimeProvider
    _scene_manager: GameSceneManager
    _fireball_factory: WizardFireballFactory
    _asset_manager: AssetManager
    _sprite: Surface

    _size: Vector2
    _position: Vector2
    _velocity: Vector2
    _current_state: WizardState
    _current_state_duration: int  # time we have spent since switching to this state

    def __init__(
            self,
            clock: GameTimeProvider,
            scene_manager: GameSceneManager,
            fireball_factory: WizardFireballFactory,
            asset_manager: AssetManager):
        self._clock = clock
        self._scene_manager = scene_manager
        self._fireball_factory = fireball_factory
        self._asset_manager = asset_manager

        self._size = Vector2(64, 64)
        # This is the starting position for new wizards
        self._position = Vector2(0, 518)
        self._velocity = Vector2(1, 0)
        self._current_state = WizardState.WALKING
        self._current_state_duration = 0

    def update(self) -> None:
        # A bit hacky but we flip the direction the wizard is moving
        # When ever they get close to the edges of the screen
        if self._position.x > 1015:
            self._velocity = Vector2(-1, 0)
        elif self._position.x < 10:
            self._velocity = Vector2(1, 0)

        if self._should_fire():
            self._attack()

        delta = self._clock.get_time()
        self._current_state_duration += delta
        logger.info(self._current_state_duration)

        if self._current_state == WizardState.ATTACKING:
            if self._current_state_duration > 2000:
                fireball = self._fireball_factory.create(self._position)
                self._scene_manager.get_scene_objects().add(fireball)
                self._walk()

        self._position = self._position + (self._velocity * delta / 10)

    def _should_fire(self) -> bool:
        if self._current_state == WizardState.ATTACKING:
            return False

        rnd = random() * 10000
        return self._current_state_duration / 1000 > rnd

    def _attack(self) -> None:
        if self._current_state == WizardState.ATTACKING:
            return

        self._set_state(WizardState.ATTACKING)
        self._velocity = Vector2(0, 0)

    def _walk(self) -> None:
        if self._current_state == WizardState.WALKING:
            return

        self._set_state(WizardState.WALKING)
        self._velocity = Vector2(1, 0)

    def _set_state(self, state: WizardState) -> None:
        self._current_state = state
        self._current_state_duration = 0

    def render(self, surface: Surface) -> None:
        sprite = self._get_sprite().copy().convert_alpha()
        radius = self._size.x / 2
        blit_position = self._position - Vector2(radius)
        surface.blit(sprite, (blit_position.x, blit_position.y))

    def _get_sprite(self) -> Surface:
        frames = {
            WizardState.WALKING: self._walking_frames(),
            WizardState.ATTACKING: self._attacking_frames(),
            WizardState.STANDING: self._standing_frames(),
        }[self._current_state]

        current_walking_frame = (self._current_state_duration / 300) % len(frames)
        return frames[int(current_walking_frame)]

    @lru_cache()
    def _walking_frames(self) -> List[Surface]:
        return [
            self._sprite_sheet_slice(Rect((64 * 0, 0), (64, 64))),
            self._sprite_sheet_slice(Rect((64 * 1, 0), (64, 64))),
        ]

    @lru_cache()
    def _attacking_frames(self) -> List[Surface]:
        return [
            self._sprite_sheet_slice(Rect((64 * 2, 0), (64, 64))),
            self._sprite_sheet_slice(Rect((64 * 3, 0), (64, 64))),
            self._sprite_sheet_slice(Rect((64 * 4, 0), (64, 64))),
        ]

    @lru_cache()
    def _standing_frames(self) -> List[Surface]:
        return [
            self._sprite_sheet_slice(Rect((64 * 0, 0), (64, 64))),
            self._sprite_sheet_slice(Rect((64 * 2, 0), (64, 64))),
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

    def is_destroyed(self) -> bool:
        return False


class SimpleWizardFactory:
    _clock: GameTimeProvider
    _scene_manager: GameSceneManager
    _fireball_factory: WizardFireballFactory
    _asset_manager: AssetManager

    def __init__(
            self,
            clock: GameTimeProvider,
            scene_manager: GameSceneManager,
            fireball_factory: WizardFireballFactory,
            asset_manager: AssetManager):
        self._clock = clock
        self._scene_manager = scene_manager
        self._fireball_factory = fireball_factory
        self._asset_manager = asset_manager

    def create(self) -> SimpleWizard:
        return SimpleWizard(
            clock=self._clock,
            scene_manager=self._scene_manager,
            fireball_factory=self._fireball_factory,
            asset_manager=self._asset_manager,
        )
