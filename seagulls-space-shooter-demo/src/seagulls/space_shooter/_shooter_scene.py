import logging
from threading import Event
from typing import Tuple

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

from ._active_scene_client import ISetActiveScene
from ._asteroid_field import AsteroidField
from ._asteroid_missed_rule import AsteroidMissedRule
from ._check_game_rules_interface import ICheckGameRules
from ._game_over_scene import GameOverSceneFactory
from ._replay_shooter_button import ReplayButtonFactory
from ._score_overlay import ScoreOverlay
from ._selectable_ship_menu import ShipSelectionMenuFactory
from ._ship import Ship
from ._ship_destroyed_rule import ShipDestroyedRule
from ._shooter_scene_client import ShooterSceneState, ShooterSceneStateClient
from ._toggleable_game_object import ToggleableGameObject

logger = logging.getLogger(__name__)


class ShooterScene(IGameScene):

    _surface_renderer: SurfaceRenderer

    _game_controls: GameControls
    _asset_manager: AssetManager
    _active_scene_manager: ISetActiveScene

    _game_objects: GameObjectsCollection
    _should_quit: Event

    _state_client: ShooterSceneStateClient
    _game_rules: Tuple[ICheckGameRules, ...]
    _background: GameObject
    _score_overlay: ScoreOverlay
    _game_over_scene_factory: GameOverSceneFactory
    _replay_button_factory: ReplayButtonFactory
    _ship_selection_menu_factory: ShipSelectionMenuFactory
    _asteriod_field: AsteroidField

    _toggleables: Tuple[ToggleableGameObject, ...]

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
            game_controls: GameControls,
            game_over_scene_factory: GameOverSceneFactory,
            replay_button_factory: ReplayButtonFactory,
            ship_selection_menu_factory: ShipSelectionMenuFactory):

        self._surface_renderer = surface_renderer
        self._asset_manager = asset_manager
        self._active_scene_manager = active_scene_manager
        self._game_controls = game_controls
        self._background = background
        self._score_overlay = score_overlay
        self._game_over_scene_factory = game_over_scene_factory
        self._replay_button_factory = replay_button_factory
        self._ship_selection_menu_factory = ship_selection_menu_factory
        self._asteriod_field = asteroid_field

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(clock)
        self._game_objects.add(background)
        self._game_objects.add(ship)
        self._game_objects.add(space_collisions)
        self._game_objects.add(score_overlay)
        self._game_objects.add(self._game_controls)

        self._toggleables = tuple([
            ToggleableGameObject(asteroid_field)
        ])

        self._state_client = ShooterSceneStateClient()
        self._game_rules = tuple([
            AsteroidMissedRule(self._state_client, asteroid_field),
            ShipDestroyedRule(self._state_client, asteroid_field, ship),
        ])

        for item in self._toggleables:
            self._game_objects.add(item)

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
        background = Surface((1024, 600))
        self._game_objects.apply(lambda x: x.render(background))

        self._surface_renderer.render(background)

    def reset(self) -> None:
        self._asteriod_field.reset()
        self._state_client.update_state(ShooterSceneState.RUNNING)
        self._score_overlay.reset()
