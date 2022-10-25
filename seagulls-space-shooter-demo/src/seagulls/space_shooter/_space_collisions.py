import logging
from functools import lru_cache
from typing import Callable, Tuple

import pygame
from pygame import mixer
from seagulls.assets import AssetManager
from seagulls.engine import GameObject, Surface

from ._asteroid_field import AsteroidField
from ._fit_to_screen import FitToScreen
from ._ship import Ship

logger = logging.getLogger(__name__)


class SpaceCollisions(GameObject):
    _asset_manager: AssetManager
    _ship: Ship
    _asteroid_field: AsteroidField
    _fit_to_screen: FitToScreen

    def __init__(
            self,
            asset_manager: AssetManager,
            ship: Ship,
            asteroid_field: AsteroidField,
            rock_collision_callback: Callable[[], None],
            fit_to_screen: FitToScreen):
        self._asset_manager = asset_manager
        self._ship = ship
        self._asteroid_field = asteroid_field
        self._rock_collision_callback = rock_collision_callback
        self._fit_to_screen = fit_to_screen

    def tick(self) -> None:
        _remove_lasers = []
        _remove_rocks = []

        for laser in range(self._ship.get_number_of_lasers()):
            if not self._laser_on_screen_y(self._ship.get_laser_position_y(laser)):
                _remove_lasers.append(laser)
                continue
            for rock in range(self._asteroid_field.get_asteroid_field_size()):
                if self._laser_rock_collision_check(laser, rock):
                    if laser not in _remove_lasers:
                        _remove_lasers.append(laser)
                        _remove_rocks.append(rock)

        _remove_lasers.sort(reverse=True)

        for laser in _remove_lasers:

            self._ship.remove_laser(laser)

        _remove_rocks.sort(reverse=True)

        for rock in _remove_rocks:
            self._asteroid_field.remove_rock(rock)
            self._rock_collision_sound().play()
            self._rock_collision_callback()

    def render(self, surface: Surface) -> None:
        pass

    def _laser_rock_collision_check(self, laser_number: int, rock_number: int) -> bool:
        rock_rect = pygame.Rect(
            (self._asteroid_field.get_rock_position_x(rock_number),
             self._asteroid_field.get_rock_position_y(rock_number)),
            self._calculate_rock_size(rock_number))
        laser_rect = pygame.Rect(
            (self._ship.get_laser_position_x(laser_number),
             self._ship.get_laser_position_y(laser_number)),
            self._calculate_laser_size())

        return pygame.Rect.colliderect(rock_rect, laser_rect)

    def _rock_on_screen_y(self, rock_position_y: float, rock_size_y: int) -> bool:
        return rock_position_y + rock_size_y > 0

    @lru_cache()
    def _rock_collision_sound(self) -> mixer.Sound:
        mixer.init()
        return mixer.Sound(self._asset_manager.get_path("sounds/rock-explosion.ogg"))

    def _laser_on_screen_y(self, laser_position_y: float) -> bool:
        return laser_position_y + 1000 > 0

    def _calculate_rock_size(self, rock_number: int) -> Tuple[float, float]:
        return (self._fit_to_screen.get_actual_surface_width() *
                self._asteroid_field.get_rock_size_x(rock_number) / 1920,
                self._fit_to_screen.get_actual_surface_height() *
                self._asteroid_field.get_rock_size_y(rock_number) / 1080)

    def _calculate_laser_size(self) -> Tuple[float, float]:
        return (self._fit_to_screen.get_actual_surface_width() * 9 / 1920,
                self._fit_to_screen.get_actual_surface_height() * 54 / 1080)
