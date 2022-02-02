import logging
import math
from functools import lru_cache
from typing import List

import pygame
from pygame import mixer
from seagulls.assets import AssetManager
from seagulls.engine import (
    GameClock,
    GameControls,
    GameObject,
    Surface,
    Vector2
)

from ._laser import Laser
from ._ship_interfaces import IProvideActiveShip

logger = logging.getLogger(__name__)


class Ship(GameObject):
    _active_ship_manager: IProvideActiveShip
    _clock: GameClock
    _asset_manager: AssetManager
    _game_controls: GameControls
    _position: Vector2
    _velocity: Vector2
    _max_velocity: float
    _lasers: List[Laser]
    _is_new_game: bool

    def __init__(
            self,
            active_ship_manager: IProvideActiveShip,
            clock: GameClock,
            asset_manager: AssetManager,
            game_controls: GameControls):
        self._active_ship_manager = active_ship_manager
        self._clock = clock
        self._asset_manager = asset_manager
        self._game_controls = game_controls
        self._is_new_game = True
        self._velocity = Vector2(0, 0)
        self._max_velocity = 7.0
        self._lasers = []

    def tick(self) -> None:
        self._max_velocity = self._active_ship_manager.get_active_ship().velocity()
        is_moving = False

        if self._is_new_game:
            self._position = self._get_start_position()
            self._is_new_game = False

        if self._game_controls.is_left_moving():
            if self._velocity.x > 0:
                self._velocity.x = 0.0
            if math.floor(abs(self._velocity.x)) <= self._max_velocity:
                self._velocity = self._velocity + Vector2(-0.1, 0)
            is_moving = True

        if self._game_controls.is_right_moving():
            if self._velocity.x < 0:
                self._velocity.x = 0.0
            if self._velocity.x <= self._max_velocity:
                self._velocity = self._velocity + Vector2(0.1, 0)
            is_moving = True

        if self._game_controls.is_left_moving() and self._game_controls.is_right_moving():
            self._velocity.x = 0.0

        if not is_moving:
            self._velocity.x = 0.0

        if self._game_controls.should_fire():
            self._lasers.append(
                Laser(
                    self._clock,
                    self._asset_manager,
                    self._position,
                    self._get_ship_width()))

            self._laser_sound().play()

        delta = self._clock.get_time()

        self._position = self._position + (self._velocity * delta / 10)

        if self._position.x < 0:
            self._position.x = 0

        if self._position.x > self._get_display_width() - 112:
            self._position.x = self._get_display_width() - 112

        for laser in self._lasers:
            laser.tick()

    def render(self, surface: Surface) -> None:
        ship_sprite = self._get_ship_sprite()

        ship_sprite = pygame.transform.scale(
            ship_sprite,
            (self._get_ship_width(), self._get_ship_height()))

        surface.blit(ship_sprite, self._position)

        for laser in self._lasers:
            laser.render(surface)

    def _get_ship_sprite(self) -> Surface:
        return self._asset_manager.load_sprite(
            self._active_ship_manager.get_active_ship().sprite()).copy()

    def get_number_of_lasers(self) -> int:
        return len(self._lasers)

    def get_laser_position_x(self, laser_number: int) -> float:
        return self._lasers[laser_number].get_laser_position_x()

    def get_laser_position_y(self, laser_number: int) -> float:
        return self._lasers[laser_number].get_laser_position_y()

    def remove_laser(self, laser_number: int):
        self._lasers.pop(laser_number)

    def get_ship_position(self) -> Vector2:
        return self._position

    def reset(self) -> None:
        self._is_new_game = True

    @lru_cache()
    def _laser_sound(self) -> mixer.Sound:
        mixer.init()
        return mixer.Sound("assets/sounds/laser-sound.ogg")

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h

    @lru_cache()
    def _get_start_position(self) -> Vector2:
        return Vector2(
            self._get_display_width() / 2 - self._get_ship_width(),
            self._get_display_height() - self._get_ship_height()
        )

    @lru_cache()
    def _get_ship_width(self) -> float:
        return self._get_display_width() / 1920 * self._get_ship_sprite().get_width()

    @lru_cache()
    def _get_ship_height(self) -> float:
        return self._get_display_height() / 1080 * self._get_ship_sprite().get_height()
