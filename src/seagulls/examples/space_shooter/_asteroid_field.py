import logging
from functools import lru_cache

import random
from typing import List, Tuple

from seagulls.engine import GameObject, Surface, GameClock, Vector2, GameObjectsCollection
from seagulls.assets import AssetManager
from ._collidables import Collidable, CollidablesCollection

logger = logging.getLogger(__name__)


class SpaceRock(GameObject, Collidable):

    _clock: GameClock
    _asset_manager: AssetManager
    _rock_size: Tuple
    _position: Vector2
    _velocity: Vector2

    _has_collided: bool

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager,
            rock_size: Tuple,
            position: Vector2):
        self._clock = clock
        self._asset_manager = asset_manager
        self._rock_size = rock_size
        self._position = position
        self._velocity = self._set_velocity(rock_size)

        self._has_collided = False

    def tick(self):
        if self._has_collided:
            return

        delta = self._clock.get_time()
        self._position = self._position + (self._velocity * delta / 200)

    def render(self, surface: Surface) -> None:
        if self._has_collided:
            return

        if self._rock_size[0] == 28:
            surface.blit(self._get_cached_rock_small(), self._position)
        elif self._rock_size[0] == 45:
            surface.blit(self._get_cached_rock_med(), self._position)
        else:
            surface.blit(self._get_cached_rock_large(), self._position)

    def check_collision(self, position: Vector2) -> bool:
        if self._has_collided:
            return False

        x = self._position.x
        y = self._position.y

        w = self._rock_size[0]
        h = self._rock_size[1]

        return x < position.x < x + w and y < position.y < y + h

    def collide(self) -> None:
        self._has_collided = True

    @lru_cache()
    def _get_cached_rock_small(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/rock-small").copy()

    @lru_cache()
    def _get_cached_rock_med(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/rock-med").copy()

    @lru_cache()
    def _get_cached_rock_large(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/rock-large").copy()

    def _set_velocity(self, rock_size: Tuple) -> Vector2:
        if rock_size == (28, 28):
            return Vector2(0, 4)
        elif rock_size == (45, 40):
            return Vector2(0, 10)
        else:
            return Vector2(0, 16)


class AsteroidField(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _next_rock_position: Vector2

    _rocks: GameObjectsCollection
    _collidables: CollidablesCollection

    def __init__(
            self,
            clock: GameClock,
            collidables: CollidablesCollection,
            asset_manager: AssetManager):
        self._clock = clock
        self._collidables = collidables
        self._asset_manager = asset_manager
        self._rocks = GameObjectsCollection()

        self._next_rock_position = Vector2(50, 30)

    def spawn_asteroids(self, num: int) -> None:
        for rock in self._create_rocks(num):
            self._rocks.add(rock)
            self._collidables.add(rock)

    def tick(self) -> None:
        self._rocks.apply(lambda x: x.tick())

    def render(self, surface: Surface) -> None:
        self._rocks.apply(lambda x: x.render(surface))

    def _create_rocks(self, num: int) -> List[SpaceRock]:
        _result = []
        for x in range(num):
            rock_size = random.randint(0, 2)
            if rock_size == 0:
                _result.append(
                    SpaceRock(
                        self._clock,
                        self._asset_manager,
                        (28, 28),
                        self._next_rock_position))
            elif rock_size == 1:
                _result.append(
                    SpaceRock(
                        self._clock,
                        self._asset_manager,
                        (45, 40),
                        self._next_rock_position))
            elif rock_size == 2:
                _result.append(
                    SpaceRock(
                        self._clock,
                        self._asset_manager,
                        (120, 98),
                        self._next_rock_position))
            self._next_rock_position = Vector2(
                self._next_rock_position.x + 140,
                self._new_rock_position_y(self._next_rock_position))

        return _result

    def _new_rock_position_y(self, rock_position: Vector2) -> float:
        random_number = random.randint(-70, 70)
        if rock_position.y + random_number < 0:
            random_number = random.randint(0, 70)
            return rock_position.y + random_number
        else:
            return rock_position.y+random_number
