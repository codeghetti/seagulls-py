import logging
import random
from functools import lru_cache
from typing import List

import pygame
from seagulls.assets import AssetManager
from seagulls.engine import GameClock, GameObject, Surface, Vector2

from ._fit_to_screen import FitToScreen
from ._space_rock import SpaceRock

logger = logging.getLogger(__name__)


class AsteroidField(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _fit_to_screen: FitToScreen
    _asteroid_field: List[SpaceRock]
    _spawn_timer: int

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager,
            fit_to_screen: FitToScreen):
        self._clock = clock
        self._asset_manager = asset_manager
        self._fit_to_screen = fit_to_screen
        self._asteroid_field = []
        self._spawn_timer = 0

    def tick(self) -> None:
        self._spawn_timer += self._clock.get_time()

        for rock in self._asteroid_field:
            rock.tick()

        if self._spawn_timer > 800:
            self._asteroid_field.append(self._spawn_one_rock())
            self._spawn_timer = 0

    def render(self, surface: Surface) -> None:
        for rock in self._asteroid_field:
            rock.render(surface)

    def _spawn_one_rock(self) -> SpaceRock:

        rock_size = random.randint(0, 2)
        rock_options = [(28, 28), (45, 40), (120, 98)]

        return SpaceRock(
                self._clock,
                self._asset_manager,
                rock_options[rock_size],
                self._get_random_rock_position(),
                self._fit_to_screen)

    def _get_random_rock_position(self) -> Vector2:
        ship_laser_buffer = 70
        return Vector2(
            random.randint(
                int(self._fit_to_screen.get_x_boundaries()[0] + ship_laser_buffer),
                int(self._fit_to_screen.get_x_boundaries()[1] - 125 - ship_laser_buffer)),
            int(self._fit_to_screen.get_y_boundaries()[0] - 100))

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

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    def remove_rock(self, rock_number: int) -> None:
        self._asteroid_field.pop(rock_number)

    def set_game_over(self) -> None:
        self._is_game_over = True

    def reset(self) -> None:
        self._asteroid_field = []
        self._spawn_timer = 0
