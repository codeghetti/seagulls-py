import logging
from functools import lru_cache
from threading import Event
from typing import Tuple

import pygame
from seagulls.assets import AssetManager
from seagulls.engine import (
    GameControls,
    GameObject,
    GameObjectsCollection,
    IGameScene,
    ISetActiveScene,
    Surface,
    SurfaceRenderer
)

from ._fit_to_screen import FitToScreen
from ._ship_button import ShipButton
from ._ship_catalog import ShipCatalog
from ._ship_interfaces import ISetActiveShip, IShip

logger = logging.getLogger(__name__)


class ShipSelectionMenu(IGameScene):
    _catalog: ShipCatalog
    _surface_renderer: SurfaceRenderer

    _scene: IGameScene
    _game_controls: GameControls
    _asset_manager: AssetManager
    _active_scene_manager: ISetActiveScene
    _active_ship_manager: ISetActiveShip

    _game_objects: GameObjectsCollection
    _should_quit: Event

    _fit_to_screen: FitToScreen

    def __init__(
            self,
            catalog: ShipCatalog,
            surface_renderer: SurfaceRenderer,
            scene: IGameScene,
            game_controls: GameControls,
            asset_manager: AssetManager,
            active_scene_manager: ISetActiveScene,
            active_ship_manager: ISetActiveShip,
            background: GameObject,
            fit_to_screen: FitToScreen):

        self._catalog = catalog
        self._surface_renderer = surface_renderer
        self._scene = scene
        self._asset_manager = asset_manager
        self._game_controls = game_controls
        self._active_scene_manager = active_scene_manager
        self._active_ship_manager = active_ship_manager

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(self._game_controls)
        self._game_objects.add(background)
        self._fit_to_screen = fit_to_screen

        self._should_quit = Event()

    def _get_ships(self) -> Tuple[IShip, ...]:
        return self._catalog.ships

    def start(self) -> None:
        for ship in self._get_ships():
            self._game_objects.add(ShipButton(
                ship,
                self._scene,
                self._asset_manager,
                self._game_controls,
                self._active_scene_manager,
                self._active_ship_manager,
                self._fit_to_screen))

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
        background = Surface((self._get_display_width(), self._get_display_height()))
        self._game_objects.apply(lambda x: x.render(background))

        self._surface_renderer.render(background)

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h


class ShipSelectionMenuFactory:
    _ship_catalog: ShipCatalog
    _surface_renderer: SurfaceRenderer

    _game_controls: GameControls
    _asset_manager: AssetManager
    _active_scene_manager: ISetActiveScene
    _active_ship_manager: ISetActiveShip
    _fit_to_screen: FitToScreen

    def __init__(
            self,
            catalog: ShipCatalog,
            surface_renderer: SurfaceRenderer,
            game_controls: GameControls,
            asset_manager: AssetManager,
            active_scene_manager: ISetActiveScene,
            active_ship_manager: ISetActiveShip,
            background: GameObject,
            fit_to_screen: FitToScreen):
        self._ship_catalog = catalog
        self._surface_renderer = surface_renderer
        self._game_controls = game_controls
        self._asset_manager = asset_manager
        self._active_scene_manager = active_scene_manager
        self._active_ship_manager = active_ship_manager
        self.background = background
        self._fit_to_screen = fit_to_screen

    @lru_cache()
    def get_instance(self, scene: IGameScene) -> ShipSelectionMenu:
        return ShipSelectionMenu(
            self._ship_catalog,
            self._surface_renderer,
            scene,
            self._game_controls,
            self._asset_manager,
            self._active_scene_manager,
            self._active_ship_manager,
            self.background,
            self._fit_to_screen)
