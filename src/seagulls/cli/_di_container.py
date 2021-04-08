from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Dependency
from seagulls.assets import AssetManager
from seagulls.attacks import WizardFireballFactory
from seagulls.pygame import GameWindowFactory, GameControls, GameSceneManager
from seagulls.pygame import GameClock
from seagulls.scenes import SimpleScene
from seagulls.ui import DebugHud
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

    _scene_manager = Singleton(GameSceneManager)

    _debug_hud = Singleton(
        DebugHud,
        scene_manager=_scene_manager,
        controls=_game_controls,
        clock=_game_clock,
    )

    _fireball_factory = Singleton(
        WizardFireballFactory,
        clock=_game_clock,
        scene_manager=_scene_manager,
        asset_manager=_asset_manager,
    )

    _wizard_factory = Singleton(
        SimpleWizardFactory,
        scene_manager=_scene_manager,
        fireball_factory=_fireball_factory,
        clock=_game_clock,
        asset_manager=_asset_manager,
    )
    _simple_scene = Singleton(
        SimpleScene,
        asset_manager=_asset_manager,
        wizard_factory=_wizard_factory,
        debug_hud=_debug_hud,
    )

    root_command = Singleton(SeagullsCommand)
    launch_command = Singleton(
        LaunchCommand,
        window_factory=_window_factory,
        scene=_simple_scene,
        scene_manager=_scene_manager,
        clock=_game_clock,
        controls=_game_controls,
    )

    example_command = Singleton(ExampleCommand)
