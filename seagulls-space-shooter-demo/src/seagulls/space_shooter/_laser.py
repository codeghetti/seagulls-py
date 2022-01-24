from functools import lru_cache

from seagulls.assets import AssetManager
from seagulls.engine import GameClock, GameObject, Surface, Vector2


class Laser(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _position: Vector2
    _velocity: Vector2

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager,
            ship_position: Vector2):
        self._clock = clock
        self._asset_manager = asset_manager
        self._position = Vector2(ship_position.x + 52, ship_position.y - 57)
        self._velocity = Vector2(0, 8)

    def tick(self) -> None:
        delta = self._clock.get_time()

        self._position = self._position - (self._velocity * delta / 10)

    def render(self, surface: Surface) -> None:
        laser_sprite = self._get_cached_laser()
        surface.blit(laser_sprite, self._position)

    @lru_cache()
    def _get_cached_laser(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/laser-red").copy()

    def get_laser_position_x(self) -> float:
        return self._position.x

    def get_laser_position_y(self) -> float:
        return self._position.y
