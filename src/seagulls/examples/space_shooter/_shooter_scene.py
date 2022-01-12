import logging
from functools import lru_cache
from threading import Event
from typing import Tuple

from pygame import mixer

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

from seagulls.examples import ISetActiveScene

from ._asteroid_field import AsteroidField
from ._asteroid_missed_rule import AsteroidMissedRule
from ._check_game_rules_interface import ICheckGameRules
from ._score_overlay import ScoreOverlay
from ._ship import Ship
from ._ship_destroyed_rule import ShipDestroyedRule
from ._shooter_scene_client import ShooterSceneState, ShooterSceneStateClient
from ._toggleable_game_object import ToggleableGameObject

logger = logging.getLogger(__name__)


class ShooterScene(IGameScene):

    _surface_renderer: SurfaceRenderer

    _scene: IGameScene
    _game_controls: GameControls
    _asset_manager: AssetManager
    _active_scene_manager: ISetActiveScene

    _game_objects: GameObjectsCollection
    _should_quit: Event

    _state_client: ShooterSceneStateClient
    _game_rules: Tuple[ICheckGameRules, ...]

    _toggleables: Tuple[ToggleableGameObject, ...]

    def __init__(
            self,
            clock: GameClock,
            surface_renderer: SurfaceRenderer,
            scene: IGameScene,
            asset_manager: AssetManager,
            active_scene_manager: ISetActiveScene,
            background: GameObject,
            ship: Ship,
            asteroid_field: AsteroidField,
            space_collisions: GameObject,
            score_overlay: ScoreOverlay,
            game_controls: GameControls):

        self._surface_renderer = surface_renderer
        self._scene = scene
        self._asset_manager = asset_manager
        self._active_scene_manager = active_scene_manager
        self._game_controls = game_controls

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

    @lru_cache()
    def _end_game(self) -> None:
        for item in self._toggleables:
            item.toggle()
        self._active_scene_manager.set_active_scene(self._scene)

    def _render(self) -> None:
        background = Surface((1024, 600))
        self._game_objects.apply(lambda x: x.render(background))

        self._surface_renderer.render(background)
