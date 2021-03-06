import logging

import pygame
from seagulls.assets import AssetManager
from seagulls.engine import GameClock, GameObject, Surface, Vector2

from ._fit_to_screen import FitToScreen

logger = logging.getLogger(__name__)


class Laser(GameObject):
    _clock: GameClock
    _asset_manager: AssetManager
    _position: Vector2
    _velocity: Vector2
    _fit_to_screen: FitToScreen

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager,
            laser_position: Vector2,
            fit_to_screen: FitToScreen):
        self._clock = clock
        self._asset_manager = asset_manager
        self._fit_to_screen = fit_to_screen
        self._position = laser_position
        self._velocity = Vector2(0, 8)

    def tick(self) -> None:
        delta = self._clock.get_time()

        self._position = self._position - (self._velocity * delta / 10)

    def render(self, surface: Surface) -> None:
        laser_sprite = self._get_sprite()

        laser_sprite = pygame.transform.scale(
            laser_sprite,
            (self._get_laser_width(), self._get_laser_height()))

        surface.blit(laser_sprite, self._position)

    def _get_sprite(self) -> Surface:
        return self._asset_manager.load_sprite("space-shooter/laser-red").copy()

    def get_laser_position_x(self) -> float:
        return self._position.x

    def get_laser_position_y(self) -> float:
        return self._position.y

    def _get_laser_width(self) -> float:
        return (
                self._fit_to_screen.get_actual_surface_width() *
                self._get_sprite().get_width() /
                1920)

    def _get_laser_height(self) -> float:
        return (self._fit_to_screen.get_actual_surface_height() *
                self._get_sprite().get_height()
                / 1080)
