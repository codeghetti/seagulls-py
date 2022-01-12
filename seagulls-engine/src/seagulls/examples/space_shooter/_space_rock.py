import logging
from functools import lru_cache
from typing import Tuple

from seagulls.assets import AssetManager
from seagulls.engine import GameClock, GameObject, Surface, Vector2

logger = logging.getLogger(__name__)


class SpaceRock(GameObject):
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
