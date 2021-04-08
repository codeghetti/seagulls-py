import logging
from datetime import datetime
from functools import lru_cache

from seagulls.assets import AssetManager
from seagulls.pygame import (
    GameScene,
    Surface, GameObject, GameSceneObjects,
)
from seagulls.ui import DebugHud
from seagulls.wizards import (
    SimpleWizardFactory,
)

logger = logging.getLogger(__name__)


class SimpleScene(GameScene):

    _asset_manager: AssetManager
    _wizard_factory: SimpleWizardFactory

    _start_time: datetime
    _last_spawn_time: datetime

    _game_objects: GameSceneObjects
    _debug_hud: DebugHud

    def __init__(
            self,
            asset_manager: AssetManager,
            wizard_factory: SimpleWizardFactory,
            debug_hud: DebugHud):

        self._asset_manager = asset_manager
        self._wizard_factory = wizard_factory

        self._ticks = 0

        self._game_objects = GameSceneObjects()
        self._debug_hud = debug_hud

    def start(self) -> None:
        self._game_objects.clear()
        self._game_objects.add(self._debug_hud)
        self._start_time = datetime.now()
        self._spawn_wizard()

    def exit(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def update(self) -> None:
        now = datetime.now()
        spawn_delay = 1.5  # Seconds between wizard spawns

        self._game_objects.update()

        if (now - self._last_spawn_time).total_seconds() > spawn_delay:
            self._spawn_wizard()

        for obj in self._game_objects.get_objects():
            obj.update()

    def render(self, surface: Surface) -> None:
        background = self._get_background().copy()

        for obj in self._game_objects.get_objects():
            obj.render(background)

        surface.blit(background, (0, 0))

    def _spawn_wizard(self) -> None:
        self.add_game_object(self._wizard_factory.create())
        self._last_spawn_time = datetime.now()

    def add_game_object(self, obj: GameObject) -> None:
        self._game_objects.add(obj)

    def get_scene_objects(self) -> GameSceneObjects:
        return self._game_objects

    @lru_cache()
    def _get_background(self) -> Surface:
        # Start with the sky and render the other environment items on top of it
        surface = self._asset_manager.load_sprite("environment/environment-sky")

        things = [
            # These need to be in the order they should be rendered on top of the sky
            self._asset_manager.load_sprite("environment/environment-stars"),
            self._asset_manager.load_sprite("environment/environment-wall"),
            self._asset_manager.load_sprite("environment/environment-bookshelves"),
            self._asset_manager.load_sprite("environment/environment-ladders"),
            self._asset_manager.load_sprite("environment/environment-floor"),
            self._asset_manager.load_sprite("environment/environment-rampart"),
            self._asset_manager.load_sprite("environment/environment-perch"),
            self._asset_manager.load_sprite("environment/environment-scrolls"),
            self._asset_manager.load_sprite("environment/environment-spider"),
        ]

        for thing in things:
            surface.blit(thing, (0, 0))

        return surface
