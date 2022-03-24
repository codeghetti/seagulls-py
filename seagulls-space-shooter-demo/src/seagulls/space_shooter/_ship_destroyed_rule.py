import logging
from typing import Tuple

import pygame

from ._asteroid_field import AsteroidField
from ._check_game_rules_interface import ICheckGameRules
from ._fit_to_screen import FitToScreen
from ._ship import Ship
from ._shooter_scene_client import ShooterSceneState, ShooterSceneStateClient

logger = logging.getLogger(__name__)


class ShipDestroyedRule(ICheckGameRules):
    _state_client: ShooterSceneStateClient
    _asteroid_field: AsteroidField
    _ship: Ship
    _fit_to_screen: FitToScreen

    def __init__(
            self,
            state_client: ShooterSceneStateClient,
            asteroid_field: AsteroidField,
            ship: Ship,
            fit_to_screen: FitToScreen):
        self._state_client = state_client
        self._asteroid_field = asteroid_field
        self._ship = ship
        self._fit_to_screen = fit_to_screen

    def check(self) -> None:
        for index in range(self._asteroid_field.get_asteroid_field_size()):
            if self._ship_rock_collision_check(index):
                self._state_client.update_state(ShooterSceneState.LOST)
                return

    def _ship_rock_collision_check(self, rock_number: int) -> bool:
        ship_position = self._ship.get_ship_position()

        rock_rect = pygame.Rect(
            (self._asteroid_field.get_rock_position_x(rock_number),
             self._asteroid_field.get_rock_position_y(rock_number)),
            self._calculate_rock_size(rock_number))

        ship_body_rect = pygame.Rect(
            (ship_position.x, ship_position.y + self._ship_height() * 0.5),
            (self._ship_width(), self._ship_height() * 0.5))

        ship_nose_rect = pygame.Rect(
            (ship_position.x + self._ship_width() * (1/3), ship_position.y),
            (self._ship_width() * (1/3), self._ship_height() * 0.5))

        return (
                       pygame.Rect.colliderect(rock_rect, ship_body_rect) or
                       pygame.Rect.colliderect(rock_rect, ship_nose_rect))

    def _calculate_rock_size(self, rock_number: int) -> Tuple[float, float]:
        return (self._fit_to_screen.get_actual_surface_width() *
                self._asteroid_field.get_rock_size_x(rock_number) / 1920,
                self._fit_to_screen.get_actual_surface_height() *
                self._asteroid_field.get_rock_size_y(rock_number) / 1080)

    def _ship_width(self) -> float:
        return self._fit_to_screen.get_actual_surface_width() * 112 / 1920

    def _ship_height(self) -> float:
        return self._fit_to_screen.get_actual_surface_height() * 75 / 1080

    def _calculate_ship_size(self) -> Tuple[float, float]:
        return (self._fit_to_screen.get_actual_surface_width() * 112 / 1920,
                self._fit_to_screen.get_actual_surface_height() * 75 / 1080)
