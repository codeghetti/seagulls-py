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
        remove_lasers = []
        remove_rocks = []

        for laser in range(len(self._ship.lasers)):
            for asteroid in range(len(self._asteroid_field.rocks)):
                if self._asteroid_field.rocks[asteroid]._position.x <= \
                        self._ship.lasers[laser]._position.x <= \
                        self._asteroid_field.rocks[asteroid]._position.x + 120:
                    if self._asteroid_field.rocks[asteroid]._position.y <= \
                            self._ship.lasers[laser]._position.y <= \
                            self._asteroid_field.rocks[asteroid]._position.y + 120:
                        logger.info("COLLIDE")
                        remove_lasers.append(laser)
                        remove_rocks.append(asteroid)
        for laser in remove_lasers:
            self._ship.lasers.pop(laser)

        for asteroid in remove_rocks:
            self._asteroid_field.rocks.pop(asteroid)

    def render(self, surface: Surface) -> None:
        pass
