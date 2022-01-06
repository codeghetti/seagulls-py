import logging
import random
from functools import lru_cache
from typing import List, Tuple

from seagulls.assets import AssetManager
from seagulls.engine import GameClock, GameObject, Surface, Vector2

logger = logging.getLogger(__name__)


class SpaceRocks(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _rock_size: Tuple
    _position: Vector2
    _velocity: Vector2

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

    def tick(self):
        delta = self._clock.get_time()
        self._position = self._position + (self._velocity * delta / 200)

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
    _asteroid_field: List[SpaceRocks]
    _is_game_over: bool
    _spawn_timer: int

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager):
        self._clock = clock
        self._asset_manager = asset_manager
        self._asteroid_field = []
        self._is_game_over = False
        self._spawn_timer = 0

    def tick(self) -> None:
        self._spawn_timer += self._clock.get_time()

        for rock in self._asteroid_field:
            rock.tick()

        if self._spawn_timer > 800:
            self._asteroid_field.append(self._spawn_one_rock())
            self._spawn_timer = 0

        if self._is_game_over:
            return

    def render(self, surface: Surface) -> None:
        for rock in self._asteroid_field:
            rock.render(surface)

    def _spawn_one_rock(self) -> SpaceRocks:

        rock_size = random.randint(0, 2)
        rock_options = [(28, 28), (45, 40), (120, 98)]

        return SpaceRocks(
                self._clock,
                self._asset_manager,
                rock_options[rock_size],
                self._get_random_rock_position())

    def _get_random_rock_position(self) -> Vector2:
        return Vector2(random.randint(0, 1024 - 125), -200)

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

    def remove_rock(self, rock_number: int) -> None:
        self._asteroid_field.pop(rock_number)

    def set_game_over(self) -> None:
        self._is_game_over = True
