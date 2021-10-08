import logging
from functools import lru_cache
from threading import Event

from seagulls.assets import AssetManager
from seagulls.engine import (
    IGameScene,
    SurfaceRenderer,
    GameObjectsCollection,
    GameControls,
    Surface,
    GameObject,
    IProvideGameScenes,
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


class MainMenuScene(IGameScene):

    _surface_renderer: SurfaceRenderer
    _game_controls: GameControls

    _game_objects: GameObjectsCollection
    _should_quit: Event

    def __init__(
            self,
            surface_renderer: SurfaceRenderer,
            background: GameObject,
            game_controls: GameControls):
        self._surface_renderer = surface_renderer
        self._game_controls = game_controls

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(background)
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


class MainMenuSceneManager(IProvideGameScenes):
    _scene: MainMenuScene

    def __init__(self, scene: MainMenuScene):
        self._scene = scene

    def get_scene(self) -> IGameScene:
        return self._scene
