import logging

from seagulls.engine import GameObject, Surface
from seagulls.examples.space_shooter import Ship, AsteroidField

logger = logging.getLogger(__name__)


class SpaceCollisions(GameObject):
    _ship: Ship
    _asteroid_field: AsteroidField

    def __init__(
            self,
            ship: Ship,
            asteroid_field: AsteroidField):
        self._ship = ship
        self._asteroid_field = asteroid_field

    def tick(self) -> None:
        _remove_lasers = []
        _remove_rocks = []

        for laser in range(self._ship.get_number_of_lasers()):
            for asteroid in range(self._asteroid_field.get_asteroid_field_size()):
                if self._asteroid_field.get_rock_position_x(asteroid) <= \
                        self._ship.get_laser_position_x(laser) <= \
                        self._asteroid_field.get_rock_position_x(asteroid) + \
                        self._asteroid_field.get_rock_size_x(asteroid):
                    if self._asteroid_field.get_rock_position_y(asteroid) <= \
                            self._ship.get_laser_position_y(laser) <= \
                            self._asteroid_field.get_rock_position_y(asteroid) + \
                            self._asteroid_field.get_rock_size_y(asteroid):
                        _remove_lasers.append(laser)
                        _remove_rocks.append(asteroid)
        for laser in _remove_lasers:
            self._ship._lasers.pop(laser)

        for asteroid in _remove_rocks:
            self._asteroid_field._rocks.pop(asteroid)

    def render(self, surface: Surface) -> None:
        pass
