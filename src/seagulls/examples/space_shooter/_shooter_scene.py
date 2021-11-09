import logging
from threading import Event

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

logger = logging.getLogger(__name__)


class ShooterScene(IGameScene):

    _surface_renderer: SurfaceRenderer
    _game_controls: GameControls
    _asset_manager: AssetManager

    _game_objects: GameObjectsCollection
    _should_quit: Event

    def __init__(
            self,
            clock: GameClock,
            surface_renderer: SurfaceRenderer,
            asset_manager: AssetManager,
            background: GameObject,
            ship: GameObject,
            game_controls: GameControls):
        self._surface_renderer = surface_renderer
        self._asset_manager = asset_manager
        self._game_controls = game_controls

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(clock)
        self._game_objects.add(background)
        self._game_objects.add(ship)
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
