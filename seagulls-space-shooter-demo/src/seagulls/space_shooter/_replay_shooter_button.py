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

from ._fit_to_screen import FitToScreen

logger = logging.getLogger(__name__)


class ReplayShooterButton(GameObject):

    _scene: IGameScene

    _asset_manager: AssetManager
    _game_controls: GameControls
    _is_highlighted: Event
    _is_clicked: Event

    _button_height = 49
    _button_width = 190

    _active_scene_manager: ISetActiveScene

    _fit_to_screen: FitToScreen

    def __init__(
            self,
            scene: IGameScene,
            asset_manager: AssetManager,
            game_controls: GameControls,
            active_scene_manager: ISetActiveScene,
            fit_to_screen: FitToScreen):

        self._scene = scene
        self._asset_manager = asset_manager
        self._game_controls = game_controls
        self._active_scene_manager = active_scene_manager
        self._fit_to_screen = fit_to_screen

        self._is_highlighted = Event()
        self._is_clicked = Event()

        self._font = Font(Path("assets/fonts/kenvector-future.ttf"), 14)

    def tick(self) -> None:
        self._detect_state()

    def render(self, surface: Surface) -> None:
        button = self._get_background()

        text = self._font.render("Play Again", True, (90, 90, 70))
        text = pygame.transform.scale(
            text,
            (self._fit_to_screen.get_actual_surface_width() * text.get_width() / 1920,
             self._fit_to_screen.get_actual_surface_height() * text.get_height() / 1080
             ))
        text_height = text.get_height()
        padding = (button.get_height() - text_height) / 2

        button.blit(text, (10, padding))

        surface.blit(button, self._get_position())

    def _detect_state(self) -> None:
        rect = Rect(self._get_position(), (self._button_width, self._button_height))
        if rect.collidepoint(pygame.mouse.get_pos()):
            self._is_highlighted.set()
            click = self._game_controls.is_click_initialized()
            if click:
                logger.debug("CLICKY")
                self._is_clicked.set()
            if not self._game_controls.is_mouse_down():
                if self._is_clicked.is_set():
                    logger.debug("SWITCH")
                    self._active_scene_manager.set_active_scene(self._scene)
                self._is_clicked.clear()
        else:
            self._is_highlighted.clear()
            self._is_clicked.clear()

    def _get_background(self) -> Surface:
        return self._get_background_map()[self._get_state_name()]

    @lru_cache()
    def _get_background_map(self) -> Dict[str, Surface]:
        return {
            "normal": self._get_blue_button(),
            "hover": self._get_green_button_0(),
            "click": self._get_green_button_1(),
        }

    def _get_blue_button(self) -> Surface:
        sprite = self._asset_manager.load_png("ui/blue.button00").copy()
        sprite = pygame.transform.scale(
            sprite,
            (self._fit_to_screen.get_actual_surface_width() * sprite.get_width() / 1920,
             self._fit_to_screen.get_actual_surface_height() * sprite.get_height() / 1080
             ))

        return sprite

    def _get_green_button_0(self) -> Surface:
        sprite = self._asset_manager.load_png("ui/green.button00").copy()
        sprite = pygame.transform.scale(
            sprite,
            (self._fit_to_screen.get_actual_surface_width() * sprite.get_width() / 1920,
             self._fit_to_screen.get_actual_surface_height() * sprite.get_height() / 1080
             ))

        return sprite

    def _get_green_button_1(self) -> Surface:
        sprite = self._asset_manager.load_png("ui/green.button01").copy()
        sprite = pygame.transform.scale(
            sprite,
            (self._fit_to_screen.get_actual_surface_width() * sprite.get_width() / 1920,
             self._fit_to_screen.get_actual_surface_height() * sprite.get_height() / 1080
             ))

        return sprite

    def _get_state_name(self) -> str:
        if self._is_highlighted.is_set():
            return "click" if self._is_clicked.is_set() else "hover"

        return "normal"

    def _get_position(self) -> Tuple[int, int]:
        left = int((self._get_display_width() / 2 + 40) - self._button_width / 2)
        top = int((self._get_display_height() / 2 + 100) - self._button_height / 2)
        if self._is_clicked.is_set():
            top += 5

        return left, top

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h


class ReplayButtonFactory:
    _asset_manager: AssetManager
    _game_controls: GameControls
    _active_scene_manager: ISetActiveScene

    def __init__(
            self,
            asset_manager: AssetManager,
            game_controls: GameControls,
            active_scene_manager: ISetActiveScene,
            fit_to_screen: FitToScreen):
        self._asset_manager = asset_manager
        self._game_controls = game_controls
        self._active_scene_manager = active_scene_manager
        self._fit_to_screen = fit_to_screen

    def get_instance(self, scene: IGameScene) -> ReplayShooterButton:
        return ReplayShooterButton(
            scene,
            self._asset_manager,
            self._game_controls,
            self._active_scene_manager,
            self._fit_to_screen)
