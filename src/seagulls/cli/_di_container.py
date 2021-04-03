from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Dependency
from seagulls.assets import AssetManager
from seagulls.pygame import GameWindowFactory, GameControls
from seagulls.pygame import GameClock
from seagulls.scenes import SimpleScene
from seagulls.wizards import SimpleWizardFactory

from ._example_command import ExampleCommand
from ._launch_command import LaunchCommand
from ._framework import LoggingClient
from ._seagulls_command import SeagullsCommand


class SeagullsDiContainer(DeclarativeContainer):
    _logging_verbosity = Dependency(instance_of=int)
    logging_client = Singleton(
        LoggingClient,
        verbosity=_logging_verbosity,
    )

    _game_clock = Singleton(GameClock)
    _game_controls = Singleton(GameControls)
    _window_factory = Singleton(GameWindowFactory)
    _asset_manager = Singleton(
        AssetManager,
        assets_path=Path("assets"),
    )
    _wizard_factory = Singleton(
        SimpleWizardFactory,
        asset_manager=_asset_manager,
        clock=_game_clock,
        controls=_game_controls,
    )
    _simple_scene = Singleton(
        SimpleScene,
        asset_manager=_asset_manager,
        wizard_factory=_wizard_factory,
    )

    root_command = Singleton(SeagullsCommand)
    launch_command = Singleton(
        LaunchCommand,
        window_factory=_window_factory,
        scene=_simple_scene,
        clock=_game_clock,
        controls=_game_controls,
    )

    example_command = Singleton(ExampleCommand)
