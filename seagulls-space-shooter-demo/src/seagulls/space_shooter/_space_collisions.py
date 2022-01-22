import logging
from typing import Callable

from pygame import mixer

from seagulls.engine import GameObject, Surface

from ._asteroid_field import AsteroidField
from ._ship import Ship

logger = logging.getLogger(__name__)


class SpaceCollisions(GameObject):
    _ship: Ship
    _asteroid_field: AsteroidField

    def __init__(
            self,
            ship: Ship,
            asteroid_field: AsteroidField,
            rock_collision_callback: Callable[[], None]):
        self._ship = ship
        self._asteroid_field = asteroid_field
        self._rock_collision_callback = rock_collision_callback
        mixer.init()
        self._rock_collision_sound = mixer.Sound("assets/sounds/rock-explosion.ogg")

    def tick(self) -> None:
        _remove_lasers = []
        _remove_rocks = []

        for laser in range(self._ship.get_number_of_lasers()):
            for rock in range(self._asteroid_field.get_asteroid_field_size()):
                if self._laser_rock_collision_check_x(laser, rock):
                    if self._laser_rock_collision_check_y(laser, rock):
                        _remove_lasers.append(laser)
                        _remove_rocks.append(rock)

        for laser in _remove_lasers:
            self._ship.remove_laser(laser)

        for rock in _remove_rocks:
            self._asteroid_field.remove_rock(rock)
            self._rock_collision_sound.play()
            self._rock_collision_callback()

    def render(self, surface: Surface) -> None:
        pass

    def _laser_rock_collision_check_x(self, laser_number: int, rock_number: int) -> bool:
        return self._asteroid_field.get_rock_position_x(rock_number) <= \
                        self._ship.get_laser_position_x(laser_number) <= \
                        self._asteroid_field.get_rock_position_x(rock_number) + \
                        self._asteroid_field.get_rock_size_x(rock_number)

    def _laser_rock_collision_check_y(self, laser_number: int, rock_number: int) -> bool:
        rock_position_y = self._asteroid_field.get_rock_position_y(rock_number)
        rock_size_y = self._asteroid_field.get_rock_size_y(rock_number)

        return (rock_position_y <=
                self._ship.get_laser_position_y(laser_number) <=
                rock_position_y +
                rock_size_y) and self._rock_on_screen_y(rock_position_y, rock_size_y)

    def _rock_on_screen_y(self, rock_position_y: float, rock_size_y: int) -> bool:
        return rock_position_y + rock_size_y > 0
