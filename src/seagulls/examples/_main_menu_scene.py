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
    GameObjectsCollection,
    IGameScene,
    IProvideGameScenes,
    Rect,
    Surface,
    SurfaceRenderer
)

logger = logging.getLogger(__name__)


class MainMenuBackground(GameObject):

    _asset_manager: AssetManager

    def __init__(self, asset_manager: AssetManager):
        self._asset_manager = asset_manager

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        background = self._get_cached_background()
        surface.blit(background, (0, 0))

    @lru_cache()
    def _get_cached_background(self) -> Surface:
        return self._asset_manager.load_sprite("environment/environment-stars").copy()


class MenuButton(GameObject):

    _asset_manager: AssetManager
    _game_controls: GameControls

    _is_highlighted: Event
    _is_clicked: Event

    _window_height = 768
    _window_width = 1024

    _button_height = 49
    _button_width = 190

    _window_scene: WindowScene

    def __init__(self, asset_manager: AssetManager, game_controls: GameControls, window_scene: WindowScene):
        self._asset_manager = asset_manager
        self._game_controls = game_controls

        self._is_highlighted = Event()
        self._is_clicked = Event()

        self._font = Font(Path("assets/fonts/kenvector-future.ttf"), 24)

    def tick(self) -> None:
        self._detect_state()

    def render(self, surface: Surface) -> None:
        button = self._get_background()

        text = self._font.render("Button", True, (90, 90, 70))
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
                    #_active_scene=shooter_scene
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


class MainMenuScene(IGameScene):

    _surface_renderer: SurfaceRenderer
    _game_controls: GameControls
    _asset_manager: AssetManager

    _game_objects: GameObjectsCollection
    _should_quit: Event

    def __init__(
            self,
            surface_renderer: SurfaceRenderer,
            asset_manager: AssetManager,
            background: GameObject,
            game_controls: GameControls):
        self._surface_renderer = surface_renderer
        self._asset_manager = asset_manager
        self._game_controls = game_controls

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(background)
        self._game_objects.add(MenuButton(
            asset_manager=asset_manager,
            game_controls=game_controls,
        ))
        self._game_objects.add(self._game_controls)

        self._should_quit = Event()

    def start(self) -> None:
        self._surface_renderer.start()
        self.tick()

    def should_quit(self) -> bool:
        return self._should_quit.is_set()

    def tick(self) -> None:
        self._game_objects.apply(lambda x: x.tick())

        if self._game_controls.should_quit():
            logger.debug("QUIT EVENT DETECTED")
            self._should_quit.set()

        self._render()

    def _render(self) -> None:
        background = Surface((1024, 600))
        self._game_objects.apply(lambda x: x.render(background))

        self._surface_renderer.render(background)


class WindowScene(IGameScene):
    _active_scene: IGameScene

    def __init__(self, active_scene: IGameScene):
        self._active_scene = active_scene

    def start(self) -> None:
        self._active_scene.start()

    def should_quit(self) -> bool:
        return self._active_scene.should_quit()

    def tick(self) -> None:
        self._active_scene.tick()


class MainMenuSceneManager(IProvideGameScenes):
    _scene: MainMenuScene

    def __init__(self, scene: MainMenuScene):
        self._scene = scene

    def get_scene(self) -> IGameScene:
        return self._scene
