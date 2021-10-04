from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton
from seagulls.assets import AssetManager
from seagulls.engine import GameClock, GameControls
from seagulls.prefabs import AsyncGameSessionManager

from ._seagulls_command import SeagullsCommand
from ._example_command import ExampleCommand
from ._launch_command import LaunchCommand
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

    # _debug_hud = Singleton(
    #     DebugHud,
    #     scene_manager=_scene_manager,
    #     controls=_game_controls,
    #     clock=_game_clock,
    # )

    # _fireball_factory = Singleton(
    #     WizardFireballFactory,
    #     clock=_game_clock,
    #     scene_manager=_scene_manager,
    #     asset_manager=_asset_manager,
    # )

    # _wizard_factory = Singleton(
    #     SimpleWizardFactory,
    #     scene_manager=_scene_manager,
    #     fireball_factory=_fireball_factory,
    #     clock=_game_clock,
    #     asset_manager=_asset_manager,
    # )
    # _player_seagull = Singleton(
    #     PlayerSeagull,
    #     controls=_game_controls,
    #     clock=_game_clock,
    #     scene_manager=_scene_manager,
    #     asset_manager=_asset_manager,
    # )
    # _simple_scene = Singleton(
    #     SimpleScene,
    #     player=_player_seagull,
    #     asset_manager=_asset_manager,
    #     wizard_factory=_wizard_factory,
    #     debug_hud=_debug_hud,
    # )

    _game_session_manager = Singleton(AsyncGameSessionManager)

    root_command = Singleton(SeagullsCommand)
    launch_command = Singleton(
        LaunchCommand,
        game_session_manager=_game_session_manager,
    )

    example_command = Singleton(ExampleCommand)
