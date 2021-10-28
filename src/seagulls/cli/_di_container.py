from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from seagulls.assets import AssetManager
from seagulls.cli._example_command import ExampleCommand
from seagulls.cli._launch_command import LaunchCommand
from seagulls.cli._seagulls_command import SeagullsCommand
from seagulls.debug import DebugHud
from seagulls.engine import GameClock, GameControls, SurfaceRenderer
from seagulls.examples import (
    AsyncGameSession,
    BlockingGameSession,
    ExampleSceneManager,
    MainMenuScene,
    SimpleStarsBackground,
    SimpleRpgBackground,
    WindowScene,
    GameState
)
from seagulls.examples.seagulls import SeagullsScene
from seagulls.examples.space_shooter import ShooterScene, Ship
from seagulls.examples.rpg import RpgScene, Character

from ._framework import LoggingClient


class SeagullsDiContainer(DeclarativeContainer):
    _logging_verbosity = Dependency(instance_of=int)
    logging_client = Singleton(
        LoggingClient,
        verbosity=_logging_verbosity,
    )

    _game_state = Singleton(GameState)
    _game_clock = Singleton(GameClock)
    _game_controls = Singleton(GameControls)
    _asset_manager = Singleton(
        AssetManager,
        assets_path=Path("assets"),
    )
    _debug_hud = Singleton(
        DebugHud,
        game_clock=_game_clock,
    )
    _surface_renderer = Singleton(SurfaceRenderer)

    _main_menu_background = Singleton(
        SimpleStarsBackground,
        asset_manager=_asset_manager,
    )

    _rpg_background = Singleton(
        SimpleRpgBackground,
        asset_manager=_asset_manager,
    )

    _ship = Singleton(
        Ship,
        clock=_game_clock,
        asset_manager=_asset_manager,
        game_controls=_game_controls,
    )

    _space_shooter_scene = Singleton(
        ShooterScene,
        clock=_game_clock,
        surface_renderer=_surface_renderer,
        asset_manager=_asset_manager,
        background=_main_menu_background,
        ship=_ship,
        game_controls=_game_controls
    )

    _seagulls_scene = Singleton(
        SeagullsScene,
    )

    _rpg_character = Singleton(
        Character,
        clock=_game_clock,
        asset_manager=_asset_manager,
        game_controls=_game_controls,
    )

    _rpg_scene = Singleton(
        RpgScene,
        surface_renderer=_surface_renderer,
        debug_hud=_debug_hud,
        clock=_game_clock,
        asset_manager=_asset_manager,
        background=_rpg_background,
        character=_rpg_character,
        game_controls=_game_controls
    )

    _main_menu_scene = Singleton(
        MainMenuScene,
        surface_renderer=_surface_renderer,
        asset_manager=_asset_manager,
        background=_main_menu_background,
        game_controls=_game_controls,
        game_state=_game_state,
        space_shooter_scene=_space_shooter_scene,
        seagulls_scene=_seagulls_scene,
        rpg_scene=_rpg_scene,
    )

    _window_scene = Singleton(
        WindowScene,
        active_scene=_main_menu_scene,
        game_state=_game_state,
    )

    _main_menu_scene_manager = Singleton(
        ExampleSceneManager,
        scene=_window_scene,
    )
    _game_session = Singleton(
        AsyncGameSession,
        scene_manager=_main_menu_scene_manager,
    )
    _blocking_game_session = Singleton(
        BlockingGameSession,
        scene_manager=_main_menu_scene_manager,
    )

    root_command = Singleton(SeagullsCommand)
    launch_command = Singleton(
        LaunchCommand,
        game_session=_blocking_game_session,
    )

    example_command = Singleton(ExampleCommand)
