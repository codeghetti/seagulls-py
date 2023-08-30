from functools import lru_cache
from pathlib import Path
from typing import Dict

import sys

from seagulls.assets import AssetManager
from seagulls.engine import (
    EmptyScene,
    GameClock,
    GameControls,
    SurfaceRenderer
)
from seagulls.pygame import PygameCameraPrinter, WindowSurface
from seagulls.rendering import (
    Camera,
    Position,
    Size,
    SpriteClient,
    SpriteInfo,
    SpritesType
)
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
from ._rpg_scene_2 import RpgScene2, SceneProvider, Sprites
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
            window=self._window(),
            camera=self._camera(),
            sprite_client=self._sprite_client(),
            game_controls=self._game_controls(),
            clock=self._clock(),
            asset_manager=self._asset_manager(),
        )

    @lru_cache()
    def _sprite_client(self) -> SpriteClient:
        return SpriteClient(
            printer=self._printer(),
            sprite_mapping=self._sprite_mapping(),
        )

    @lru_cache()
    def _sprite_mapping(self) -> Dict[SpritesType, SpriteInfo]:
        asset_client = self._asset_manager()
        assets = str(asset_client.get_path(
            "kenney.pixel-platformer-farm-expansion/Tilemap/tilemap-packed.png").resolve())
        medieval = str(asset_client.get_path("kenney.medieval-pack/medieval-packed.png").resolve())
        ghost = str(
            asset_client.get_path("kenney.tiny-dungeon/Tilemap/tilemap-packed.png").resolve())
        hearts = str(
            asset_client.get_path("kenney.pixel-platformer/Tilemap/tiles_packed.png").resolve())
        game_over = str(asset_client.get_path(
            "kenney.shooting-gallery-pack/PNG/HUD/text_gameover.png").resolve())
        menu_button = str(asset_client.get_path(
            "kenney.ui-pack-rpg-expansion/PNG/buttonLong_brown.png").resolve())

        return {
            Sprites.floor_left_corner: SpriteInfo(
                path=assets,
                resolution=(288, 126),
                size=(18, 18),
                game_size=(50, 50),
                coordinates=(18, 0),
            ),
            Sprites.floor_middle: SpriteInfo(
                path=assets,
                resolution=(288, 126),
                size=(18, 18),
                game_size=(50, 50),
                coordinates=(36, 0),
            ),
            Sprites.floor_right_corner: SpriteInfo(
                path=assets,
                resolution=(288, 126),
                size=(18, 18),
                game_size=(50, 50),
                coordinates=(54, 0),
            ),
            Sprites.floor_single_piece: SpriteInfo(
                path=assets,
                resolution=(288, 126),
                size=(18, 18),
                game_size=(50, 50),
                coordinates=(0, 0),
            ),
            Sprites.pumpkin: SpriteInfo(
                path=assets,
                resolution=(288, 126),
                size=(18, 18),
                game_size=(35, 35),
                coordinates=(90, 0),
            ),

            Sprites.dead_pumpkin: SpriteInfo(
                path=assets,
                resolution=(288, 126),
                size=(18, 18),
                game_size=(35, 35),
                coordinates=(72, 0),
            ),

            Sprites.ghost: SpriteInfo(
                path=ghost,
                resolution=(192, 176),
                size=(16, 16),
                game_size=(50, 50),
                coordinates=(16, 160),
            ),

            Sprites.sword: SpriteInfo(
                path=ghost,
                resolution=(192, 176),
                size=(16, 16),
                game_size=(35, 35),
                coordinates=(112, 128),
            ),

            Sprites.full_health: SpriteInfo(
                path=hearts,
                resolution=(360, 162),
                size=(18, 18),
                game_size=(50, 50),
                coordinates=(72, 36),
            ),

            Sprites.half_health: SpriteInfo(
                path=hearts,
                resolution=(360, 162),
                size=(18, 18),
                game_size=(50, 50),
                coordinates=(90, 36),
            ),

            Sprites.zero_health: SpriteInfo(
                path=hearts,
                resolution=(360, 162),
                size=(18, 18),
                game_size=(50, 50),
                coordinates=(108, 36),
            ),

            Sprites.game_over: SpriteInfo(
                path=game_over,
                resolution=(349, 72),
                size=(349, 72),
                game_size=(484, 100),
                coordinates=(0, 0),
            ),
            Sprites.flag_banner: SpriteInfo(
                path=medieval,
                resolution=(1024, 2048),
                size=(70, 70),
                game_size=(50, 50),
                coordinates=(280, 420),
            ),
            Sprites.flag_pole: SpriteInfo(
                path=medieval,
                resolution=(1024, 2048),
                size=(70, 70),
                game_size=(50, 50),
                coordinates=(140, 1260),
            ),
            Sprites.green_ghost: SpriteInfo(
                path=ghost,
                resolution=(192, 176),
                size=(16, 16),
                game_size=(35, 35),
                coordinates=(0, 144)
            ),
            Sprites.menu_button: SpriteInfo(
                path=menu_button,
                resolution=(190, 49),
                size=(190, 49),
                game_size=(300, 80),
                coordinates=(0, 0),
            ),
        }

    @lru_cache()
    def _printer(self) -> PygameCameraPrinter:
        return PygameCameraPrinter(
            surface=self._window(),
            camera=self._camera()
        )

    @lru_cache()
    def _window(self) -> WindowSurface:
        return WindowSurface(
            resolution_setting={"height": 600, "width": 1000},
            camera_setting=self._camera_size().get()
        )

    @lru_cache()
    def _camera(self) -> Camera:
        return Camera(
            size=self._camera_size(),
            position=Position({"x": 0, "y": 0})
        )

    @lru_cache()
    def _camera_size(self) -> Size:
        return Size(
            size={"height": 600, "width": 1000}
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
