import logging
import math
from functools import lru_cache

from seagulls.assets import AssetManager
from seagulls.engine import GameObject, Surface, GameControls, Vector2, GameClock

logger = logging.getLogger(__name__)


class Ship(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _game_controls: GameControls
    _position: Vector2
    _velocity: Vector2
    _max_velocity: float

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager,
            game_controls: GameControls):
        self._clock = clock
        self._asset_manager = asset_manager
        self._game_controls = game_controls
        self._position = Vector2(400, 303)
        self._velocity = Vector2(0, 0)
        self._max_velocity = 7.0

    def tick(self) -> None:
        if self._game_controls.is_left_moving():
            if math.floor(abs(self._velocity.x)) <= self._max_velocity:
                self._velocity = self._velocity + Vector2(-0.1, 0)
        elif self._game_controls.is_right_moving():
            if self._velocity.x <= self._max_velocity:
                self._velocity = self._velocity + Vector2(0.1, 0)
        else:
            self._velocity.x = 0.0
        if self._game_controls.is_up_moving():
            if math.floor(abs(self._velocity.y)) <= self._max_velocity:
                self._velocity = self._velocity + Vector2(0, -0.1)
        elif self._game_controls.is_down_moving():
            if self._velocity.y <= self._max_velocity:
                self._velocity = self._velocity + Vector2(0, 0.1)
        else:
            self._velocity.y = 0.0

        delta = self._clock.get_time()

        self._position = self._position + (self._velocity * delta / 10)

        if self._position.x < 0:
            self._position.x = 0

        if self._position.x > 1024 - 112:
            self._position.x = 1024 - 112

        if self._position.y < 0:
            self._position.y = 0

        if self._position.y > 600 - 75:
            self._position.y = 600 - 75

    def render(self, surface: Surface) -> None:
        background = self._get_cached_background()
        surface.blit(background, self._position)

    @lru_cache()
    def _get_cached_background(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/ship-orange").copy()
