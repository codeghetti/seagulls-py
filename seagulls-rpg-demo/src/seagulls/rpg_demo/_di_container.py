import sys
from functools import lru_cache
from pathlib import Path

from seagulls.assets import AssetManager
from seagulls.engine import (
    EmptyScene,
    GameClock,
    GameControls,
    SurfaceRenderer
)
from seagulls.pygame import PygamePrinter, WindowSurface
from seagulls.seagulls_cli import (
    SeagullsAppDiContainer,
    SeagullsCliApplication,
    SeagullsRuntimeClient
)
from seagulls.session import BlockingGameSession, NullGameSession

from ._character import Character
from ._cli_command import GameCliCommand
from ._cli_plugin import RpgDemoCliPlugin
from ._debug_hud import DebugHud
from ._fit_to_screen import FitToScreen
from ._homes_and_trees import HomesAndTrees
from ._pygame_screen import PygameScreen
from ._rpg_background import SimpleRpgBackground
from ._rpg_scene_2 import RpgScene2, SceneProvider
from ._screen_provider import ScreenProvider
from ._session import RpgSessionProvider


class RpgDemoDiContainer:
    _application: SeagullsCliApplication

    def __init__(self, application: SeagullsCliApplication):
        self._application = application

    @lru_cache()
    def plugin(self) -> RpgDemoCliPlugin:
        return RpgDemoCliPlugin(
            application=self._application,
            command=self._command(),
        )

    @lru_cache()
    def _command(self) -> GameCliCommand:
        return GameCliCommand(
            game_session=self._blocking_game_session(),
            scene=self._rpg_scene(),
            window=self._window()
        )

    @lru_cache()
    def _blocking_game_session(self) -> BlockingGameSession:
        return BlockingGameSession(
            screen_provider=self._screen_provider()
        )

    @lru_cache()
    def _screen_provider(self) -> ScreenProvider:
        return ScreenProvider(
            screen=self._screen()
        )

    @lru_cache()
    def _screen(self) -> PygameScreen:
        return PygameScreen(
            scene=self._scene_provider()
        )

    @lru_cache()
    def _scene_provider(self) -> SceneProvider:
        return SceneProvider(
            scene=self._rpg_scene()
        )

    @lru_cache()
    def _empty_scene(self) -> EmptyScene:
        return EmptyScene()

    @lru_cache()
    def _rpg_scene(self) -> RpgScene2:
        return RpgScene2(
            session=self._rpg_session_provider(),
            printer=self._printer(),
            window=self._window()
        )

    @lru_cache()
    def _printer(self) -> PygamePrinter:
        return PygamePrinter(
            surface=self._window()
        )

    @lru_cache()
    def _window(self) -> WindowSurface:
        return WindowSurface(
            resolution_setting={"height": 600, "width": 1000},
            camera_setting={"height": 600, "width": 1000}
        )

    @lru_cache()
    def _rpg_session_provider(self) -> RpgSessionProvider:
        return RpgSessionProvider(
            session=self._null_game_session()
        )

    @lru_cache()
    def _null_game_session(self) -> NullGameSession:
        return NullGameSession()

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

    @lru_cache()
    def _find_assets_path(self) -> Path:
        if self._runtime_client().is_bundled():
            return Path(f"{getattr(sys, '_MEIPASS')}/seagulls_assets")

        container_dir_path = Path(__file__).parent
        parts = str(container_dir_path.resolve()).split("/site-packages/")
        if len(parts) == 2:
            return Path(parts[0]) / "site-packages/seagulls_assets"

        return Path("seagulls_assets")

    @lru_cache()
    def _runtime_client(self) -> SeagullsRuntimeClient:
        return self._seagulls_app_container().runtime_client()

    @lru_cache()
    def _seagulls_app_container(self) -> SeagullsAppDiContainer:
        return self._application.get_container(SeagullsAppDiContainer)
