from functools import lru_cache
from pathlib import Path

from seagulls.assets import AssetManager
from seagulls.debug import DebugHud
from seagulls.engine import (
    ActiveSceneClient,
    EmptyScene,
    GameClock,
    GameControls,
    SurfaceRenderer,
    WindowScene
)
from seagulls.seagulls_cli import SeagullsCliApplication

from seagulls.rpg_demo._blocking_game_session import BlockingGameSession
from seagulls.rpg_demo._character import Character
from seagulls.rpg_demo._cli_command import GameCliCommand
from seagulls.rpg_demo._cli_plugin import RpgDemoCliPlugin
from seagulls.rpg_demo._example_scene_manager import ExampleSceneManager
from seagulls.rpg_demo._rpg_background import SimpleRpgBackground
from seagulls.rpg_demo._rpg_scene import RpgScene


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
            scene_manager=ExampleSceneManager(scene=self._window_scene()))

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
            character=self._character(),
            game_controls=self._game_controls(),
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
        )

    @lru_cache()
    def _surface_renderer(self) -> SurfaceRenderer:
        return SurfaceRenderer()

    @lru_cache()
    def _debug_hud(self) -> DebugHud:
        return DebugHud(game_clock=self._clock())

    @lru_cache()
    def _clock(self) -> GameClock:
        return GameClock()

    @lru_cache()
    def _game_controls(self) -> GameControls:
        return GameControls()

    @lru_cache()
    def _asset_manager(self) -> AssetManager:
        return AssetManager(assets_path=Path("assets"))
