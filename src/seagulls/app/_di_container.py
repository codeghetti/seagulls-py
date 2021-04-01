from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Dependency
from seagulls.assets import AssetManager
from seagulls.pygame._game_client import PygameClient
from seagulls.scenes._simple import SimpleScene

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

    _pygame_client = Singleton(PygameClient)
    _asset_manager = Singleton(
        AssetManager,
        assets_path=Path("assets"),
    )
    _simple_scene = Singleton(
        SimpleScene,
        asset_manager=_asset_manager,
    )

    root_command = Singleton(RootCommand)
    launch_command = Singleton(
        LaunchCommand,
        pygame_client=_pygame_client,
        scene=_simple_scene,
    )

    example_command = Singleton(ExampleCommand)
