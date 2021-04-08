import logging
from enum import Enum, auto
from functools import lru_cache
from typing import List

import pygame
from seagulls.assets import AssetManager
from seagulls.pygame import (
    GameTimeProvider,
    Vector2,
    Surface,
    Rect,
    GameObject,
    GameSceneObjects, GameSceneManager,
)

logger = logging.getLogger(__name__)


class WizardFireballState(Enum):
    SEEKING = auto()
    EXPLODING = auto()


class WizardFireball(GameObject):

    _clock: GameTimeProvider
    _scene_manager: GameSceneManager
    _asset_manager: AssetManager
    _sprite: Surface

    _size: Vector2
    _position: Vector2
    _velocity: Vector2
    _current_state: WizardFireballState
    _current_state_duration: int  # time we have spent since switching to this state

    def __init__(
            self,
            clock: GameTimeProvider,
            scene_manager: GameSceneManager,
            asset_manager: AssetManager,
            starting_position: Vector2):
        self._clock = clock
        self._scene_manager = scene_manager
        self._asset_manager = asset_manager

        self._size = Vector2(64, 64)

        self._position = starting_position
        self._velocity = Vector2(0, -1)
        self._current_state = WizardFireballState.SEEKING
        self._current_state_duration = 0

    def update(self) -> None:
        delta = self._clock.get_time()
        self._current_state_duration += delta

        self._position = self._position + (self._velocity * delta / 10)

    def _set_state(self, state: WizardFireballState) -> None:
        self._current_state = state
        self._current_state_duration = 0

    def render(self, surface: Surface) -> None:
        sprite = self._get_sprite().copy().convert_alpha()
        radius = self._size.x / 2
        blit_position = self._position - Vector2(radius)
        surface.blit(sprite, (blit_position.x, blit_position.y))

    def _get_sprite(self) -> Surface:
        frames = {
            WizardFireballState.SEEKING: self._seeking_frames(),
        }[self._current_state]

        current_frame = (self._current_state_duration / 300) % len(frames)
        return frames[int(current_frame)]

    @lru_cache()
    def _seeking_frames(self) -> List[Surface]:
        return [
            self._sprite_sheet_slice(Rect((64 * 4, 0), (64, 64))),
            self._sprite_sheet_slice(Rect((64 * 5, 0), (64, 64))),
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
        return self._asset_manager.load_sprite("attacks/fireball1/fireball-spritesheet")

    def is_destroyed(self) -> bool:
        return self._position.y < 0


class WizardFireballFactory:
    _clock: GameTimeProvider
    _scene_manager: GameSceneManager
    _asset_manager: AssetManager

    def __init__(
            self,
            clock: GameTimeProvider,
            scene_manager: GameSceneManager,
            asset_manager: AssetManager):
        self._clock = clock
        self._scene_manager = scene_manager
        self._asset_manager = asset_manager

    def create(self, starting_position: Vector2) -> WizardFireball:
        return WizardFireball(
            clock=self._clock,
            scene_manager=self._scene_manager,
            asset_manager=self._asset_manager,
            starting_position=starting_position,
        )
