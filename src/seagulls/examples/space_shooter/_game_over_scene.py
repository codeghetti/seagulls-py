import logging
from functools import lru_cache
from threading import Event

from pygame import mixer, Surface

from seagulls.assets import AssetManager
from seagulls.engine import IGameScene, SurfaceRenderer, GameControls, GameObjectsCollection, \
    GameObject
from seagulls.examples import ISetActiveScene
from seagulls.examples.space_shooter import ScoreOverlay
from ._game_over_overlay import GameOverOverlay

logger = logging.getLogger(__name__)


class GameOverScene(IGameScene):
    _surface_renderer: SurfaceRenderer

    _scene: IGameScene
    _game_controls: GameControls
    _asset_manager: AssetManager
    _active_scene_manager: ISetActiveScene

    _game_objects: GameObjectsCollection
    _should_quit: Event

    _score_overlay: ScoreOverlay

    def __init__(
            self,
            surface_renderer: SurfaceRenderer,
            game_controls: GameControls,
            asset_manager: AssetManager,
            active_scene_manager: ISetActiveScene,
            score_overlay: ScoreOverlay,
            background: GameObject):
        mixer.init()
        self._surface_renderer = surface_renderer
        self._game_controls = game_controls
        self._asset_manager = asset_manager
        self._active_scene_manager = active_scene_manager

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(background)
        self._game_objects.add(score_overlay)
        self._score_overlay = score_overlay

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

        self._game_over_summary()

        self._render()

    @lru_cache()
    def _game_over_summary(self) -> None:
        mixer.Sound("assets/sounds/game-over.ogg").play()
        self._game_objects.add(GameOverOverlay())

    def _render(self) -> None:
        background = Surface((1024, 600))
        self._game_objects.apply(lambda x: x.render(background))

        self._surface_renderer.render(background)
