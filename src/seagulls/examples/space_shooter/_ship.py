import logging
import math
from functools import lru_cache
from typing import List

from pygame import mixer

from seagulls.assets import AssetManager
from seagulls.engine import (
    GameClock,
    GameControls,
    GameObject,
    Surface,
    Vector2
)

from ._selectable_ship_menu import IProvideActiveShip

logger = logging.getLogger(__name__)


class Laser(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _position: Vector2
    _velocity: Vector2

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager,
            ship_position: Vector2):
        self._clock = clock
        self._asset_manager = asset_manager
        self._position = Vector2(ship_position.x + 52, ship_position.y - 57)
        self._velocity = Vector2(0, 8)

    def tick(self) -> None:
        delta = self._clock.get_time()

        self._position = self._position - (self._velocity * delta / 10)

    def render(self, surface: Surface) -> None:
        laser_sprite = self._get_cached_laser()
        surface.blit(laser_sprite, self._position)

    @lru_cache()
    def _get_cached_laser(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/laser-red").copy()

    def get_laser_position_x(self) -> float:
        return self._position.x

    def get_laser_position_y(self) -> float:
        return self._position.y


class Ship(GameObject):
    _active_ship_manager: IProvideActiveShip
    _clock: GameClock
    _asset_manager: AssetManager
    _game_controls: GameControls
    _position: Vector2
    _velocity: Vector2
    _max_velocity: float
    _lasers: List[Laser]

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

        self._position = Vector2(400, 600 - 75)
        self._velocity = Vector2(0, 0)
        self._max_velocity = 7.0
        self._lasers = []
        mixer.init()
        self._laser_sound = mixer.Sound("assets/sounds/laser-sound.ogg")

    def tick(self) -> None:
        self._max_velocity = self._active_ship_manager.get_active_ship().velocity()
        if self._game_controls.is_left_moving():
            if math.floor(abs(self._velocity.x)) <= self._max_velocity:
                self._velocity = self._velocity + Vector2(-0.1, 0)
        elif self._game_controls.is_right_moving():
            if self._velocity.x <= self._max_velocity:
                self._velocity = self._velocity + Vector2(0.1, 0)
        else:
            self._velocity.x = 0.0

        if self._game_controls.should_fire():
            self._lasers.append(Laser(self._clock, self._asset_manager, self._position))
            self._laser_sound.play()

        delta = self._clock.get_time()

        self._position = self._position + (self._velocity * delta / 10)

        if self._position.x < 0:
            self._position.x = 0

        if self._position.x > 1024 - 112:
            self._position.x = 1024 - 112

        for laser in self._lasers:
            laser.tick()

    def render(self, surface: Surface) -> None:
        ship_sprite = self._get_ship_sprite()
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
