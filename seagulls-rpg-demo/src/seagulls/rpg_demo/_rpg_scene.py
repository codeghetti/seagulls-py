import logging
from functools import lru_cache
from threading import Event

import pygame

from seagulls.assets import AssetManager
from seagulls.engine import (
    GameClock,
    GameControls,
    GameObject,
    GameObjectsCollection,
    IGameScene,
    Surface,
    SurfaceRenderer
)
from ._fit_to_screen import FitToScreen

logger = logging.getLogger(__name__)


class RpgScene(IGameScene):

    _surface_render: SurfaceRenderer
    _clock: GameClock
    _game_controls: GameControls
    _asset_manager: AssetManager
    _game_objects: GameObjectsCollection
    _should_quit: Event
    _fit_to_screen: FitToScreen

    def __init__(
            self,
            surface_renderer: SurfaceRenderer,
            clock: GameClock,
            debug_hud: GameObject,
            asset_manager: AssetManager,
            background: GameObject,
            character: GameObject,
            game_controls: GameControls,
            fit_to_screen: FitToScreen):
        self._surface_render = surface_renderer
        self._asset_manager = asset_manager
        self._game_controls = game_controls
        self._fit_to_screen = fit_to_screen

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(clock)
        self._game_objects.add(background)
        self._game_objects.add(debug_hud)
        self._game_objects.add(character)
        self._game_objects.add(self._game_controls)

        self._should_quit = Event()

    def start(self) -> None:
        self._surface_render.start()
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
        background = pygame.transform.scale(
            background,
            (
                self._get_scaled_width(),
                self._get_scaled_height()
            )
        )
        screen_size_w = pygame.display.Info().current_w
        screen_size_h = pygame.display.Info().current_h
        screen = Surface((screen_size_w, screen_size_h))
        screen.blit(background, (self._x_padding(), self._y_padding()))
        self._surface_render.render(screen)

    @lru_cache()
    def _get_scaled_width(self) -> float:
        return self._fit_to_screen.get_actual_surface_width() * 1024 * 1.8 / 1920

    @lru_cache()
    def _get_scaled_height(self) -> float:
        return self._fit_to_screen.get_actual_surface_height() * 600 * 1.8 / 1080

    def _x_padding(self) -> float:
        screen_size_w = pygame.display.Info().current_w
        playable_w = self._get_scaled_width()
        padding = (screen_size_w - playable_w) / 2
        return padding

    def _y_padding(self) -> float:
        screen_size_h = pygame.display.Info().current_h
        playabe_h = self._get_scaled_height()
        padding = (screen_size_h - playabe_h) / 2
        return padding
