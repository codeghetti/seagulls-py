import logging

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

        nose_collision_check = (
            self._asteroid_field.get_rock_position_x(rock_number) <=
            (ship_position.x + 50) <=
            self._asteroid_field.get_rock_position_x(rock_number) +
            self._asteroid_field.get_rock_size_x(rock_number) and
            self._asteroid_field.get_rock_position_y(rock_number) <=
            ship_position.y <=
            self._asteroid_field.get_rock_position_y(rock_number) +
            self._asteroid_field.get_rock_size_y(rock_number)
        )

        left_upper_wing_check = (
            self._asteroid_field.get_rock_position_x(rock_number) <= ship_position.x <=
            self._asteroid_field.get_rock_position_x(rock_number) +
            self._asteroid_field.get_rock_size_x(rock_number) and
            self._asteroid_field.get_rock_position_y(rock_number) <=
            (ship_position.y + 30) <=
            self._asteroid_field.get_rock_position_y(rock_number) +
            self._asteroid_field.get_rock_size_y(rock_number)
        )

        right_upper_wing_check = (
            self._asteroid_field.get_rock_position_x(rock_number) <=
            (ship_position.x + 105) <=
            self._asteroid_field.get_rock_position_x(rock_number) +
            self._asteroid_field.get_rock_size_x(rock_number) and
            self._asteroid_field.get_rock_position_y(rock_number) <=
            (ship_position.y + 30) <=
            self._asteroid_field.get_rock_position_y(rock_number) +
            self._asteroid_field.get_rock_size_y(rock_number)
        )

        left_lower_wing_check = (
            self._asteroid_field.get_rock_position_x(rock_number) <= ship_position.x <=
            self._asteroid_field.get_rock_position_x(rock_number) +
            self._asteroid_field.get_rock_size_x(rock_number)
            and self._asteroid_field.get_rock_position_y(rock_number) <=
            (ship_position.y + 68) <=
            self._asteroid_field.get_rock_position_y(rock_number) +
            self._asteroid_field.get_rock_size_y(rock_number)
        )

        right_lower_wing_check = (
            self._asteroid_field.get_rock_position_x(rock_number) <=
            (ship_position.x + 105) <=
            self._asteroid_field.get_rock_position_x(rock_number) +
            self._asteroid_field.get_rock_size_x(rock_number) and
            self._asteroid_field.get_rock_position_y(rock_number) <=
            (ship_position.y + 68) <=
            self._asteroid_field.get_rock_position_y(rock_number) +
            self._asteroid_field.get_rock_size_y(rock_number)
        )

        return (
            nose_collision_check or
            left_lower_wing_check or
            right_lower_wing_check or
            left_upper_wing_check or
            right_upper_wing_check)
