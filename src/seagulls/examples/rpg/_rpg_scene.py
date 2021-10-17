import logging
from threading import Event

from seagulls.assets import AssetManager
from seagulls.engine import IGameScene, SurfaceRenderer, GameObjectsCollection, GameObject, GameControls, Surface

logger = logging.getLogger(__name__)


class RpgScene(IGameScene):

    _surface_render: SurfaceRenderer
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
        self._surface_render = surface_renderer
        self._asset_manager = asset_manager
        self._game_controls = game_controls

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(background)
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

        self._surface_render.render(background)
