import logging
from functools import lru_cache
from typing import Dict, List

import pygame
from seagulls.assets import AssetManager
from seagulls.engine import (
    GameClock,
    GameControls,
    GameObject,
    Surface,
    Vector2
)

from ._homes_and_trees import HomesAndTrees

logger = logging.getLogger(__name__)


class Character(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _game_controls: GameControls
    _homes_and_trees: HomesAndTrees
    _position: Vector2
    _velocity: Vector2

    _time: float
    _current_state: str
    _standing_position: str

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager,
            game_controls: GameControls,
            homes_and_trees: HomesAndTrees):
        self._clock = clock
        self._asset_manager = asset_manager
        self._game_controls = game_controls
        self._homes_and_trees = homes_and_trees
        self._position = Vector2(400, 303)
        self._velocity = Vector2(0, 0)
        self._time = 0.0
        self._current_state = "standing"
        self._standing_position = "down"

    def tick(self) -> None:
        self._process_movement()
        self._ensure_in_bounds()

    def _process_movement(self) -> None:
        self._time += self._clock.get_time()
        if self._game_controls.is_left_moving():
            self._walk("left")
            self._velocity = Vector2(-1, 0)
        elif self._game_controls.is_right_moving():
            self._walk("right")
            self._velocity = Vector2(1, 0)
        elif self._game_controls.is_up_moving():
            self._walk("up")
            self._velocity = Vector2(0, -1)
        elif self._game_controls.is_down_moving():
            self._walk("down")
            self._velocity = Vector2(0, 1)
        else:
            if not self._current_state.startswith("standing"):
                self._time = 0

            self._current_state = f"standing.{self._standing_position}"
            self._velocity = Vector2(0, 0)

        delta = self._clock.get_time()

        desired_position = self._position + (self._velocity * delta / 10)

        character_square = pygame.Rect(desired_position, (16, 16))

        world_objects = self._homes_and_trees.get_world_object_rectangles()
        collision = self._collision(character_square, world_objects)
        if collision == -1:
            self._position = desired_position
        else:
            if self._velocity.x != 0:
                if self._position.x > world_objects[collision].x:
                    self._position.x = world_objects[collision].x + world_objects[collision].width
                elif self._position.x < world_objects[collision].x:
                    self._position.x = world_objects[collision].x - 16
            if self._velocity.y != 0:
                if self._position.y > world_objects[collision].y + world_objects[collision].height:
                    self._position.y = world_objects[collision].y + world_objects[collision].height
                elif self._position.y < world_objects[collision].y:
                    self._position.y = world_objects[collision].y - 16

    def _collision(self, character_square: pygame.Rect, rectangles: List[pygame.Rect]):
        return character_square.collidelist(rectangles)

    def _walk(self, direction: str) -> None:
        self._standing_position = direction

        if not self._current_state.startswith(f"walking-{direction}"):
            self._current_state = f"walking-{direction}.1"
            self._time = 0.0
        elif self._is_time_to_switch():
            if self._current_state == f"walking-{direction}.1":
                self._current_state = f"walking-{direction}.2"
            elif self._current_state == f"walking-{direction}.2":
                self._current_state = f"walking-{direction}.3"
            elif self._current_state == f"walking-{direction}.3":
                self._current_state = f"walking-{direction}.4"
            else:
                self._current_state = f"walking-{direction}.1"
            self._time = 0.0

    def _ensure_in_bounds(self):
        # TODO: need to check if we are near water
        if self._position.x < 0:
            self._position.x = 0
        if self._position.x > 1024 - 16:
            self._position.x = 1024 - 16
        if self._position.y < 0:
            self._position.y = 0
        if self._position.y > 600 - 16:
            self._position.y = 600 - 16

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
