from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from seagulls.assets import AssetManager
from seagulls.cli._example_command import ExampleCommand
from seagulls.cli._launch_command import LaunchCommand
from seagulls.cli._seagulls_command import SeagullsCommand
from seagulls.engine import GameClock, GameControls, SurfaceRenderer
from seagulls.examples import AsyncGameSession, MainMenuScene, MainMenuSceneManager, \
    MainMenuBackground

from ._framework import LoggingClient


class SeagullsDiContainer(DeclarativeContainer):
    _logging_verbosity = Dependency(instance_of=int)
    logging_client = Singleton(
        LoggingClient,
        verbosity=_logging_verbosity,
    )

    _game_clock = Singleton(GameClock)
    _game_controls = Singleton(GameControls)
    _asset_manager = Singleton(
        AssetManager,
        assets_path=Path("assets"),
    )
    _surface_renderer = Singleton(SurfaceRenderer)

    _main_menu_background = Singleton(
        MainMenuBackground,
        asset_manager=_asset_manager,
    )
    _main_menu_scene = Singleton(
        MainMenuScene,
        surface_renderer=_surface_renderer,
        asset_manager=_asset_manager,
        background=_main_menu_background,
        game_controls=_game_controls,
    )
    _main_menu_scene_manager = Singleton(
        MainMenuSceneManager,
        scene=_main_menu_scene,
    )
    _game_session = Singleton(
        AsyncGameSession,
        scene_manager=_main_menu_scene_manager,
    )

    root_command = Singleton(SeagullsCommand)
    launch_command = Singleton(
        LaunchCommand,
        game_session=_game_session,
    )

    example_command = Singleton(ExampleCommand)
