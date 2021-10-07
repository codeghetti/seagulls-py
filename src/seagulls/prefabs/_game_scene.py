import random
from pathlib import Path
from threading import Event

from seagulls.assets import AssetManager
from seagulls.creatures import Bird
from seagulls.debug import DebugHud
from seagulls.engine import (
    Surface,
    IGameScene,
    SurfaceRenderer,
    GameControls,
    GameObjectsCollection,
    GameClock,
)
from seagulls.wizards import SimpleWizard

from ._background import SeagullsBackground


class SeagullGameScene(IGameScene):

    _name: str
    _asset_manager: AssetManager
    _clock: GameClock
    _surface_renderer: SurfaceRenderer
    _game_controls = GameControls
    _game_objects: GameObjectsCollection
    _should_quit: Event

    def __init__(self, name: str) -> None:
        self._name = name
        self._surface_renderer = SurfaceRenderer()
        self._asset_manager = AssetManager(Path("assets"))

        self._clock = GameClock()

        self._game_controls = GameControls()
        self._should_quit = Event()

        background = SeagullsBackground(asset_manager=self._asset_manager)

        bird = Bird(
            clock=self._clock,
            asset_manager=self._asset_manager,
            game_controls=self._game_controls,
        )

        self._game_objects = GameObjectsCollection()

        wizard = SimpleWizard(
            clock=self._clock,
            scene_objects=self._game_objects,
            asset_manager=self._asset_manager)
        debug_hud = DebugHud(self._clock)

        self._game_objects.add(self._clock)
        self._game_objects.add(self._game_controls)
        self._game_objects.add(background)
        self._game_objects.add(bird)
        self._game_objects.add(wizard)
        self._game_objects.add(debug_hud)

    def start(self) -> None:
        self._surface_renderer.start()
        self.tick()

    def should_quit(self) -> bool:
        return self._game_controls.should_quit()

    def tick(self) -> None:
        self._game_objects.apply(lambda x: x.tick())

        if self._game_controls.should_quit():
            self._should_quit.set()

        self._render()

    def _render(self) -> None:
        background = Surface((1024, 600))
        self._game_objects.apply(lambda x: x.render(background))

        self._surface_renderer.render(background)
