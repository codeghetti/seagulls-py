from functools import lru_cache

import pygame

from ._asteroid_field import AsteroidField
from ._check_game_rules_interface import ICheckGameRules
from ._fit_to_screen import FitToScreen
from ._shooter_scene_client import ShooterSceneState, ShooterSceneStateClient


class AsteroidMissedRule(ICheckGameRules):
    _state_client: ShooterSceneStateClient
    _asteroid_field: AsteroidField
    _fit_to_screen: FitToScreen

    def __init__(
            self,
            state_client: ShooterSceneStateClient,
            asteroid_field: AsteroidField,
            fit_to_screen: FitToScreen):
        self._state_client = state_client
        self._asteroid_field = asteroid_field
        self._fit_to_screen = fit_to_screen

    def check(self) -> None:
        for x in range(self._asteroid_field.get_asteroid_field_size()):
            if self._asteroid_field.get_rock_position_y(x) > \
                    self._fit_to_screen.get_y_boundaries().y:
                self._state_client.update_state(ShooterSceneState.LOST)

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h
