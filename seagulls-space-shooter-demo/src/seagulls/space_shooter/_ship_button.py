import logging
from functools import lru_cache
from pathlib import Path
from threading import Event
from typing import Dict, Tuple

import pygame
from pygame.font import Font
from seagulls.assets import AssetManager
from seagulls.engine import (
    GameControls,
    GameObject,
    IGameScene,
    ISetActiveScene,
    Rect,
    Surface
)

from ._ship_interfaces import ISetActiveShip, IShip

logger = logging.getLogger(__name__)


class ShipButton(GameObject):

    _ship: IShip
    _scene: IGameScene

    _asset_manager: AssetManager
    _game_controls: GameControls
    _is_highlighted: Event
    _is_clicked: Event

    _button_height = 49
    _button_width = 190

    _active_scene_manager: ISetActiveScene
    _active_ship_manager: ISetActiveShip

    def __init__(
            self,
            ship: IShip,
            scene: IGameScene,
            asset_manager: AssetManager,
            game_controls: GameControls,
            active_scene_manager: ISetActiveScene,
            active_ship_manager: ISetActiveShip):

        self._ship = ship
        self._scene = scene
        self._asset_manager = asset_manager
        self._game_controls = game_controls
        self._active_scene_manager = active_scene_manager
        self._active_ship_manager = active_ship_manager

        self._is_highlighted = Event()
        self._is_clicked = Event()

        self._font = Font(Path("assets/fonts/kenvector-future.ttf"), 14)

    def tick(self) -> None:
        self._detect_state()

    def render(self, surface: Surface) -> None:
        button = self._get_background()

        text = self._font.render(self._ship.display_name(), True, (90, 90, 70))
        text_height = text.get_height()
        padding = (button.get_height() - text_height) / 2

        ship_sprite = self._asset_manager.load_sprite(self._ship.sprite()).copy()
        ship_velocity = self._font.render("Velocity: " + str(self._ship.velocity()), True,
                                          "red", "black")
        ship_power = self._font.render("Power: " + str(self._ship.power()), True,
                                       "red", "black")

        button.blit(text, (10, padding))
        surface.blit(button, (self._get_position()[0], self._get_position()[1] + 160))
        surface.blit(ship_sprite, (self._get_position()[0], self._get_position()[1]))
        surface.blit(ship_velocity, (self._get_position()[0], self._get_position()[1] + 100))
        surface.blit(ship_power, (self._get_position()[0], self._get_position()[1] + 120))

    def _detect_state(self) -> None:
        rect = Rect(
            (self._get_position()[0], self._get_position()[1] + 160),
            (self._button_width,
             self._button_height))

        if rect.collidepoint(pygame.mouse.get_pos()):
            self._is_highlighted.set()
            click = self._game_controls.is_click_initialized()
            if click:
                logger.debug("CLICKY")
                self._is_clicked.set()
            if not self._game_controls.is_mouse_down():
                if self._is_clicked.is_set():
                    logger.debug("SWITCH")
                    # TODO fix typing issue below
                    self._scene.reset()  # type: ignore
                    self._active_scene_manager.set_active_scene(self._scene)
                    self._active_ship_manager.set_active_ship(self._ship)
                self._is_clicked.clear()
        else:
            self._is_highlighted.clear()
            self._is_clicked.clear()

    def _get_background(self) -> Surface:
        return self._get_background_map()[self._get_state_name()]

    @lru_cache()
    def _get_background_map(self) -> Dict[str, Surface]:
        return {
            "normal": self._asset_manager.load_png("ui/blue.button00").copy(),
            "hover": self._asset_manager.load_png("ui/green.button00").copy(),
            "click": self._asset_manager.load_png("ui/green.button01").copy(),
        }

    def _get_state_name(self) -> str:
        if self._is_highlighted.is_set():
            return "click" if self._is_clicked.is_set() else "hover"

        return "normal"

    def _get_position(self) -> Tuple[int, int]:
        left = int((self._get_display_width() / 3) - self._button_width / 2) + self._ship.offset()
        top = int((self._get_display_height() / 3) - self._button_height / 2)
        if self._is_clicked.is_set():
            top += 5

        return left, top

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h
