import sys
from functools import lru_cache
from pathlib import Path

from seagulls.assets import AssetManager
from seagulls.engine import (
    ActiveSceneClient,
    BasicSceneManager,
    BlockingGameSession,
    EmptyScene,
    GameClock,
    GameControls,
    SurfaceRenderer,
    WindowScene
)
from seagulls.seagulls_cli import (
    SeagullsAppDiContainer,
    SeagullsCliApplication,
    SeagullsRuntimeClient
)

from ._character import Character
from ._cli_command import GameCliCommand
from ._cli_plugin import RpgDemoCliPlugin
from ._debug_hud import DebugHud
from ._fit_to_screen import FitToScreen
from ._homes_and_trees import HomesAndTrees
from ._rpg_background import SimpleRpgBackground
from ._rpg_scene import RpgScene


class RpgDemoDiContainer:
    _application: SeagullsCliApplication

    def __init__(self, application: SeagullsCliApplication):
        self._application = application

    def plugin(self) -> RpgDemoCliPlugin:
        return RpgDemoCliPlugin(
            application=self._application,
            command=self._command(),
        )

    def _command(self) -> GameCliCommand:
        return GameCliCommand(
            game_session=self._blocking_game_session(),
            active_scene_manager=self._active_scene_client(),
            scene=self._rpg_scene(),
        )

    @lru_cache()
    def _blocking_game_session(self) -> BlockingGameSession:
        return BlockingGameSession(
            scene_manager=BasicSceneManager(scene=self._window_scene()))

    @lru_cache()
    def _window_scene(self) -> WindowScene:
        return WindowScene(
            active_scene_provider=self._active_scene_client(),
        )

    @lru_cache()
    def _active_scene_client(self) -> ActiveSceneClient:
        return ActiveSceneClient(scene=self._empty_scene())

    @lru_cache()
    def _empty_scene(self) -> EmptyScene:
        return EmptyScene()

    def _rpg_scene(self) -> RpgScene:
        return RpgScene(
            surface_renderer=self._surface_renderer(),
            clock=self._clock(),
            debug_hud=self._debug_hud(),
            asset_manager=self._asset_manager(),
            background=self._background(),
            homes_and_trees=self._homes_and_trees(),
            character=self._character(),
            game_controls=self._game_controls(),
            fit_to_screen=self._fit_to_screen()
        )

    @lru_cache()
    def _background(self) -> SimpleRpgBackground:
        return SimpleRpgBackground(asset_manager=self._asset_manager())

    @lru_cache()
    def _character(self) -> Character:
        return Character(
            clock=self._clock(),
            asset_manager=self._asset_manager(),
            game_controls=self._game_controls(),
            homes_and_trees=self._homes_and_trees(),
        )

    @lru_cache()
    def _homes_and_trees(self) -> HomesAndTrees:
        return HomesAndTrees(
            asset_manager=self._asset_manager()
        )

    @lru_cache()
    def _fit_to_screen(self) -> FitToScreen:
        return FitToScreen()

    @lru_cache()
    def _surface_renderer(self) -> SurfaceRenderer:
        return SurfaceRenderer()

    @lru_cache()
    def _debug_hud(self) -> DebugHud:
        return DebugHud(asset_manager=self._asset_manager(), game_clock=self._clock())

    @lru_cache()
    def _clock(self) -> GameClock:
        return GameClock()

    @lru_cache()
    def _game_controls(self) -> GameControls:
        return GameControls()

    @lru_cache()
    def _asset_manager(self) -> AssetManager:
        return AssetManager(assets_path=self._find_assets_path())

    def _find_assets_path(self) -> Path:
        if self._runtime_client().is_bundled():
            return Path(f"{getattr(sys, '_MEIPASS')}/seagulls_assets")

        container_dir_path = Path(__file__).parent
        parts = str(container_dir_path.resolve()).split("/site-packages/")
        if len(parts) == 2:
            return Path(parts[0]) / "site-packages/seagulls_assets"

        return Path("seagulls_assets")

    def _runtime_client(self) -> SeagullsRuntimeClient:
        return self._seagulls_app_container().runtime_client()

    def _seagulls_app_container(self) -> SeagullsAppDiContainer:
        return self._application.get_container(SeagullsAppDiContainer)
