import logging
from functools import lru_cache
from typing import Dict

import pygame
from seagulls.assets import AssetManager
from seagulls.engine import GameObject, Surface, GameControls, Vector2, GameClock

logger = logging.getLogger(__name__)


class Character(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _game_controls: GameControls
    _position: Vector2
    _velocity: Vector2

    _time: float
    _current_state: str
    _standing_position: str

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
        self._time = 0.0
        self._current_state = "standing"
        self._standing_position = "down"

    def tick(self) -> None:
        self._time += self._clock.get_time()

        if self._game_controls.is_left_moving():
            self._standing_position = "left"
            if not self._current_state.startswith("walking-left"):
                self._current_state = "walking-left.1"
                self._time = 0.0
            elif self._is_time_to_switch():
                if self._current_state == "walking-left.1":
                    self._current_state = "walking-left.2"
                elif self._current_state == "walking-left.2":
                    self._current_state = "walking-left.3"
                elif self._current_state == "walking-left.3":
                    self._current_state = "walking-left.4"
                else:
                    self._current_state = "walking-left.1"
                self._time = 0.0

            self._velocity = Vector2(-1, 0)
        elif self._game_controls.is_right_moving():
            self._standing_position = "right"
            if not self._current_state.startswith("walking-right"):
                self._current_state = "walking-right.1"
                self._time = 0.0
            elif self._is_time_to_switch():
                logger.info("SWITCHING!")
                if self._current_state == "walking-right.1":
                    self._current_state = "walking-right.2"
                elif self._current_state == "walking-right.2":
                    self._current_state = "walking-right.3"
                elif self._current_state == "walking-right.3":
                    self._current_state = "walking-right.4"
                else:
                    self._current_state = "walking-right.1"
                self._time = 0.0

            self._velocity = Vector2(1, 0)
        elif self._game_controls.is_up_moving():
            self._standing_position = "up"
            if not self._current_state.startswith("walking-up"):
                self._current_state = "walking-up.1"
                self._time = 0.0
            elif self._is_time_to_switch():
                if self._current_state == "walking-up.1":
                    self._current_state = "walking-up.2"
                elif self._current_state == "walking-up.2":
                    self._current_state = "walking-up.3"
                elif self._current_state == "walking-up.3":
                    self._current_state = "walking-up.4"
                else:
                    self._current_state = "walking-up.1"
                self._time = 0.0

            self._velocity = Vector2(0, -1)
        elif self._game_controls.is_down_moving():
            self._standing_position = "down"
            if not self._current_state.startswith("walking-down"):
                self._current_state = "walking-down.1"
                self._time = 0.0
            elif self._is_time_to_switch():
                if self._current_state == "walking-down.1":
                    self._current_state = "walking-down.2"
                elif self._current_state == "walking-down.2":
                    self._current_state = "walking-down.3"
                elif self._current_state == "walking-down.3":
                    self._current_state = "walking-down.4"
                else:
                    self._current_state = "walking-down.1"
                self._time = 0.0

            self._velocity = Vector2(0, 1)
        else:
            if not self._current_state.startswith("standing"):
                self._time = 0

            self._current_state = f"standing.{self._standing_position}"
            self._velocity = Vector2(0, 0)

        logger.info(f"Time: {self._time}")

        delta = self._clock.get_time()

        self._position = self._position + (self._velocity * delta / 10)

        # TODO: need to check if we are near water
        if self._position.x < 0:
            self._position.x = 0

        if self._position.x > 1024 - 112:
            self._position.x = 1024 - 112

        if self._position.y < 0:
            self._position.y = 0

        if self._position.y > 600 - 75:
            self._position.y = 600 - 75

    def _is_time_to_switch(self) -> bool:
        return self._time > 333

    def render(self, surface: Surface) -> None:
        character = self._get_character()
        camera = Surface(Vector2(16, 16), pygame.SRCALPHA, 32).convert_alpha()
        camera.blit(character, self._state_coordinates()[self._current_state])
        surface.blit(camera, self._position)

    @lru_cache()
    def _get_character(self) -> Surface:
        # This image is 27 columns and 18 rows (16x16 images)
        return self._asset_manager.load_sprite("rpg/rpg-urban-tilemap.packed").copy()

    def _state_coordinates(self) -> Dict[str, Vector2]:
        return {
            "standing.left": Vector2(23 * -16, 0 * -16),
            "standing.down": Vector2(24 * -16, 0 * -16),
            "standing.up": Vector2(25 * -16, 0 * -16),
            "standing.right": Vector2(26 * -16, 0 * -16),

            "walking-left.1": Vector2(23 * -16, 1 * -16),
            "walking-left.2": Vector2(23 * -16, 0 * -16),
            "walking-left.3": Vector2(23 * -16, 2 * -16),
            "walking-left.4": Vector2(23 * -16, 0 * -16),

            "walking-down.1": Vector2(24 * -16, 1 * -16),
            "walking-down.2": Vector2(24 * -16, 0 * -16),
            "walking-down.3": Vector2(24 * -16, 2 * -16),
            "walking-down.4": Vector2(24 * -16, 0 * -16),

            "walking-up.1": Vector2(25 * -16, 1 * -16),
            "walking-up.2": Vector2(25 * -16, 0 * -16),
            "walking-up.3": Vector2(25 * -16, 2 * -16),
            "walking-up.4": Vector2(25 * -16, 0 * -16),

            "walking-right.1": Vector2(26 * -16, 1 * -16),
            "walking-right.2": Vector2(26 * -16, 0 * -16),
            "walking-right.3": Vector2(26 * -16, 2 * -16),
            "walking-right.4": Vector2(26 * -16, 0 * -16),
        }
