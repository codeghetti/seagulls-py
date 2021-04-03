from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Dependency
from seagulls.assets import AssetManager
from seagulls.pygame._game_client import PygameClient
from seagulls.pygame._game_clock import GameClock
from seagulls.scenes._simple import SimpleScene
from seagulls.wizards._simple import SimpleWizardFactory

from ._example_command import ExampleCommand
from ._launch_command import LaunchCommand
from ._logging_client import LoggingClient
from ._root_command import RootCommand


class SeagullsDiContainer(DeclarativeContainer):
    _logging_verbosity = Dependency(instance_of=int)
    logging_client = Singleton(
        LoggingClient,
        verbosity=_logging_verbosity,
    )

    _game_clock = Singleton(GameClock)
    _pygame_client = Singleton(PygameClient)
    _asset_manager = Singleton(
        AssetManager,
        assets_path=Path("assets"),
    )
    _wizard_factory = Singleton(
        SimpleWizardFactory,
        asset_manager=_asset_manager,
        clock=_game_clock,
    )
    _simple_scene = Singleton(
        SimpleScene,
        asset_manager=_asset_manager,
        wizard_factory=_wizard_factory,
    )

    root_command = Singleton(RootCommand)
    launch_command = Singleton(
        LaunchCommand,
        pygame_client=_pygame_client,
        scene=_simple_scene,
        clock=_game_clock,
    )

    example_command = Singleton(ExampleCommand)
