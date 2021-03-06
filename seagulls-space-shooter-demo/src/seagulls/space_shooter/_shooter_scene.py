import logging
from functools import lru_cache
from threading import Event
from typing import Tuple

import pygame
from seagulls.assets import AssetManager
from seagulls.engine import (
    GameClock,
    GameControls,
    GameObject,
    GameObjectsCollection,
    IGameScene,
    ISetActiveScene,
    Surface,
    SurfaceRenderer
)

from ._asteroid_field import AsteroidField
from ._asteroid_missed_rule import AsteroidMissedRule
from ._check_game_rules_interface import ICheckGameRules
from ._fit_to_screen import FitToScreen
from ._game_over_scene import GameOverSceneFactory
from ._replay_shooter_button import ReplayButtonFactory
from ._score_overlay import ScoreOverlay
from ._score_tracker import ScoreTracker
from ._selectable_ship_menu import ShipSelectionMenuFactory
from ._ship import Ship
from ._ship_destroyed_rule import ShipDestroyedRule
from ._ship_powered_up_rule import ShipPoweredUpRule
from ._ship_state_client import ShipStateClient
from ._shooter_scene_client import ShooterSceneState, ShooterSceneStateClient

logger = logging.getLogger(__name__)


class ShooterScene(IGameScene):

    _surface_renderer: SurfaceRenderer

    _game_controls: GameControls
    _asset_manager: AssetManager
    _active_scene_manager: ISetActiveScene

    _game_objects: GameObjectsCollection
    _should_quit: Event

    _state_client: ShooterSceneStateClient
    _ship_state_client: ShipStateClient
    _game_rules: Tuple[ICheckGameRules, ...]
    _background: GameObject
    _score_overlay: ScoreOverlay
    _score_tracker: ScoreTracker
    _game_over_scene_factory: GameOverSceneFactory
    _replay_button_factory: ReplayButtonFactory
    _ship_selection_menu_factory: ShipSelectionMenuFactory
    _asteroid_field: AsteroidField
    _fit_to_screen: FitToScreen

    def __init__(
            self,
            clock: GameClock,
            surface_renderer: SurfaceRenderer,
            asset_manager: AssetManager,
            active_scene_manager: ISetActiveScene,
            background: GameObject,
            ship: Ship,
            asteroid_field: AsteroidField,
            space_collisions: GameObject,
            score_overlay: ScoreOverlay,
            score_tracker: ScoreTracker,
            game_controls: GameControls,
            game_over_scene_factory: GameOverSceneFactory,
            replay_button_factory: ReplayButtonFactory,
            ship_selection_menu_factory: ShipSelectionMenuFactory,
            fit_to_screen: FitToScreen,
            ship_state_client: ShipStateClient):

        self._surface_renderer = surface_renderer
        self._asset_manager = asset_manager
        self._active_scene_manager = active_scene_manager
        self._game_controls = game_controls
        self._background = background
        self._score_overlay = score_overlay
        self._score_tracker = score_tracker
        self._game_over_scene_factory = game_over_scene_factory
        self._replay_button_factory = replay_button_factory
        self._ship_selection_menu_factory = ship_selection_menu_factory
        self._asteroid_field = asteroid_field
        self._ship = ship
        self._fit_to_screen = fit_to_screen

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(clock)
        self._game_objects.add(background)
        self._game_objects.add(self._ship)
        self._game_objects.add(space_collisions)
        self._game_objects.add(score_overlay)
        self._game_objects.add(self._game_controls)
        self._game_objects.add(self._asteroid_field)

        self._state_client = ShooterSceneStateClient()
        self._ship_state_client = ship_state_client
        self._game_rules = tuple([
            AsteroidMissedRule(self._state_client, asteroid_field, self._fit_to_screen),
            ShipDestroyedRule(self._state_client, asteroid_field, ship, self._fit_to_screen),
            ShipPoweredUpRule(self._ship_state_client, self._score_tracker)
        ])

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

        for rule in self._game_rules:
            rule.check()

        if not self._state_client.get_state() == ShooterSceneState.RUNNING:
            self._end_game()

        self._render()

    def _end_game(self) -> None:
        ship_selection_menu_scene = self._ship_selection_menu_factory.get_instance(self)
        replay_button = self._replay_button_factory.get_instance(ship_selection_menu_scene)
        self._active_scene_manager.set_active_scene(
            self._game_over_scene_factory.get_instance(replay_button))

    def _render(self) -> None:
        background = Surface((self._get_display_width(), self._get_display_height()))
        self._game_objects.apply(lambda x: x.render(background))

        top_black_bar = Surface((
            self._get_display_width(),
            int(self._fit_to_screen.get_y_padding())))
        bottom_black_bar = Surface((
            self._get_display_width(),
            int(self._fit_to_screen.get_y_padding())))
        background.blit(top_black_bar, (0, 0))
        background.blit(bottom_black_bar, (
            0,
            self._fit_to_screen.get_y_padding() + self._fit_to_screen.get_actual_surface_height()))

        self._surface_renderer.render(background)

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h

    def reset(self) -> None:
        self._asteroid_field.reset()
        self._state_client.update_state(ShooterSceneState.RUNNING)
        self._score_overlay.reset()
        self._ship.reset()
