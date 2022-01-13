import logging
from functools import lru_cache
from pathlib import Path
from threading import Event
from typing import Dict, Tuple

import pygame
from pygame.font import Font

from seagulls.assets import AssetManager
from seagulls.engine import GameControls, GameObject, IGameScene, Rect, Surface
from seagulls.examples import ISetActiveScene

logger = logging.getLogger(__name__)


class ReplayShooterButton(GameObject):

    _scene: IGameScene

    _asset_manager: AssetManager
    _game_controls: GameControls
    _is_highlighted: Event
    _is_clicked: Event

    _window_height = 768
    _window_width = 1024

    _button_height = 49
    _button_width = 190

    _active_scene_manager: ISetActiveScene

    def __init__(
            self,
            scene: IGameScene,
            asset_manager: AssetManager,
            game_controls: GameControls,
            active_scene_manager: ISetActiveScene):

        self._scene = scene
        self._asset_manager = asset_manager
        self._game_controls = game_controls
        self._active_scene_manager = active_scene_manager

        self._is_highlighted = Event()
        self._is_clicked = Event()

        self._font = Font(Path("assets/fonts/kenvector-future.ttf"), 14)

    def tick(self) -> None:
        self._detect_state()

    def render(self, surface: Surface) -> None:
        button = self._get_background()

        text = self._font.render("Play Again", True, (90, 90, 70))
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
            "normal": self._asset_manager.load_png("ui/blue.button00").copy(),
            "hover": self._asset_manager.load_png("ui/green.button00").copy(),
            "click": self._asset_manager.load_png("ui/green.button01").copy(),
        }

    def _get_state_name(self) -> str:
        if self._is_highlighted.is_set():
            return "click" if self._is_clicked.is_set() else "hover"

        return "normal"

    def _get_position(self) -> Tuple[int, int]:
        left = int((self._window_width / 2) - self._button_width / 2)
        top = int((self._window_height / 2) - self._button_height / 2)
        if self._is_clicked.is_set():
            top += 5

        return left, top


class ReplayButtonFactory:
    _asset_manager: AssetManager
    _game_controls: GameControls
    _active_scene_manager: ISetActiveScene

    def __init__(
            self,
            asset_manager: AssetManager,
            game_controls: GameControls,
            active_scene_manager: ISetActiveScene):
        self._asset_manager = asset_manager
        self._game_controls = game_controls
        self._active_scene_manager = active_scene_manager

    def get_instance(self, scene: IGameScene) -> ReplayShooterButton:
        return ReplayShooterButton(
            scene,
            self._asset_manager,
            self._game_controls,
            self._active_scene_manager)
