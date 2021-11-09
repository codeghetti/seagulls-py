from functools import lru_cache

import random
from typing import List

from seagulls.engine import GameObject, Surface, GameClock, Vector2
from seagulls.assets import AssetManager


class SpaceRocks(GameObject):
    _asset_manager: AssetManager
    _rock_size: int
    _rock_position: Vector2

    def __init__(
            self,
            asset_manager: AssetManager,
            rock_size: int,
            rock_position: Vector2):
        self._asset_manager = asset_manager
        self._rock_size = rock_size
        self._rock_position = rock_position

    def tick(self):
        pass

    def render(self, surface: Surface) -> None:
        if self._rock_size == 0:
            surface.blit(self._get_cached_rock_small(), self._rock_position)
        elif self._rock_size == 1:
            surface.blit(self._get_cached_rock_med(), self._rock_position)
        else:
            surface.blit(self._get_cached_rock_large(), self._rock_position)

    @lru_cache()
    def _get_cached_rock_small(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/rock-small").copy()

    @lru_cache()
    def _get_cached_rock_med(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/rock-med").copy()

    @lru_cache()
    def _get_cached_rock_large(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/rock-large").copy()


class AsteroidField(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _next_rock_position: Vector2
    _rocks: List[GameObject]

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager):
        self._clock = clock
        self._asset_manager = asset_manager
        self._next_rock_position = Vector2(50, 30)
        self._rocks = []

    def tick(self) -> None:
        if len(self._rocks) < 7:
            rock_size = random.randint(0, 2)
            self._rocks.append(SpaceRocks(self._asset_manager, rock_size, self._next_rock_position))
            self._next_rock_position = Vector2(
                self._next_rock_position.x + 140,
                self._new_rock_position_y(self._next_rock_position))

    def render(self, surface: Surface) -> None:
        for rock in self._rocks:
            rock.render(surface)

    def _new_rock_position_y(self, rock_position: Vector2) -> float:
        random_number = random.randint(-70, 70)
        if rock_position.y + random_number < 0:
            random_number = random.randint(0, 70)
            return rock_position.y + random_number
        else:
            return rock_position.y+random_number
