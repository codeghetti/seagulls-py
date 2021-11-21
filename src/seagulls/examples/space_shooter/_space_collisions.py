import logging
from pathlib import Path

from pygame.font import Font

from seagulls.engine import GameObject, Surface
from seagulls.examples.space_shooter import Ship, AsteroidField

logger = logging.getLogger(__name__)


class SpaceCollisions(GameObject):
    _ship: Ship
    _asteroid_field: AsteroidField
    _collision_count: int

    def __init__(
            self,
            ship: Ship,
            asteroid_field: AsteroidField):
        self._ship = ship
        self._asteroid_field = asteroid_field
        self._collision_count = 0
        self._font = Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 18)

    def tick(self) -> None:
        _remove_lasers = []
        _remove_rocks = []

        for laser in range(self._ship.get_number_of_lasers()):
            for rock in range(self._asteroid_field.get_asteroid_field_size()):
                if self._laser_rock_collision_check_x(laser, rock):
                    if self._laser_rock_collision_check_y(laser, rock):
                        _remove_lasers.append(laser)
                        _remove_rocks.append(rock)
                        self._collision_count += 1

        for laser in _remove_lasers:
            self._ship.remove_laser(laser)

        for rock in _remove_rocks:
            self._asteroid_field.remove_rock(rock)

    def render(self, surface: Surface) -> None:
        img = self._font.render(
            f"Score: {self._collision_count}",
            True,
            "red", "black"
        )
        surface.blit(img, (920, 570))

    def _laser_rock_collision_check_x(self, laser_number: int, rock_number: int) -> bool:
        return self._asteroid_field.get_rock_position_x(rock_number) <= \
                        self._ship.get_laser_position_x(laser_number) <= \
                        self._asteroid_field.get_rock_position_x(rock_number) + \
                        self._asteroid_field.get_rock_size_x(rock_number)

    def _laser_rock_collision_check_y(self, laser_number: int, rock_number: int) -> bool:
        return self._asteroid_field.get_rock_position_y(rock_number) <= \
                            self._ship.get_laser_position_y(laser_number) <= \
                            self._asteroid_field.get_rock_position_y(rock_number) + \
                            self._asteroid_field.get_rock_size_y(rock_number)
