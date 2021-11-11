from functools import lru_cache

import random
from typing import List, Tuple

from seagulls.engine import GameObject, Surface, GameClock, Vector2
from seagulls.assets import AssetManager


class SpaceRocks(GameObject):
    _asset_manager: AssetManager
    _rock_size: Tuple
    _position: Vector2

    def __init__(
            self,
            asset_manager: AssetManager,
            rock_size: Tuple,
            position: Vector2):
        self._asset_manager = asset_manager
        self._rock_size = rock_size
        self._position = position

    def tick(self):
        pass

    def render(self, surface: Surface) -> None:
        if self._rock_size[0] == 28:
            surface.blit(self._get_cached_rock_small(), self._position)
        elif self._rock_size[0] == 45:
            surface.blit(self._get_cached_rock_med(), self._position)
        else:
            surface.blit(self._get_cached_rock_large(), self._position)

    @lru_cache()
    def _get_cached_rock_small(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/rock-small").copy()

    @lru_cache()
    def _get_cached_rock_med(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/rock-med").copy()

    @lru_cache()
    def _get_cached_rock_large(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/rock-large").copy()

    def get_rock_size_x(self) -> int:
        return self._rock_size[0]

    def get_rock_size_y(self) -> int:
        return self._rock_size[1]

    def get_rock_position_x(self) -> float:
        return self._position.x

    def get_rock_position_y(self) -> float:
        return self._position.y


class AsteroidField(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _next_rock_position: Vector2
    _asteroid_field: List[SpaceRocks]

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager):
        self._clock = clock
        self._asset_manager = asset_manager
        self._next_rock_position = Vector2(50, 30)
        self._asteroid_field = []

    def tick(self) -> None:
        if len(self._asteroid_field) < 7:
            rock_size = random.randint(0, 2)
            if rock_size == 0:
                self._asteroid_field.append(
                    SpaceRocks(self._asset_manager, (28, 28), self._next_rock_position))
            elif rock_size == 1:
                self._asteroid_field.append(
                    SpaceRocks(self._asset_manager, (45, 40), self._next_rock_position))
            elif rock_size == 2:
                self._asteroid_field.append(
                    SpaceRocks(self._asset_manager, (120, 98), self._next_rock_position))
            self._next_rock_position = Vector2(
                self._next_rock_position.x + 140,
                self._new_rock_position_y(self._next_rock_position))

    def render(self, surface: Surface) -> None:
        for rock in self._asteroid_field:
            rock.render(surface)

    def get_asteroid_field_size(self) -> int:
        return len(self._asteroid_field)

    def get_rock_size_x(self, rock_number: int) -> int:
        return self._asteroid_field[rock_number].get_rock_size_x()

    def get_rock_size_y(self, rock_number: int) -> int:
        return self._asteroid_field[rock_number].get_rock_size_y()

    def get_rock_position_x(self, rock_number: int) -> float:
        return self._asteroid_field[rock_number].get_rock_position_x()

    def get_rock_position_y(self, rock_number: int) -> float:
        return self._asteroid_field[rock_number].get_rock_position_y()

    def remove_rock(self, rock_number:int) -> None:
        self._asteroid_field.pop(rock_number)

    def _new_rock_position_y(self, rock_position: Vector2) -> float:
        random_number = random.randint(-70, 70)
        if rock_position.y + random_number < 0:
            random_number = random.randint(0, 70)
            return rock_position.y + random_number
        else:
            return rock_position.y+random_number
