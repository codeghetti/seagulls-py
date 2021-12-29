from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from seagulls.assets import AssetManager
from seagulls.cli._example_command import ExampleCommand
from seagulls.cli._launch_command import LaunchCommand
from seagulls.cli._seagulls_command import SeagullsCommand
from seagulls.debug import DebugHud
from seagulls.engine import (
    GameClock,
    GameControls,
    IGameScene,
    SurfaceRenderer
)
from seagulls.examples import (
    ActiveSceneClient,
    AsyncGameSession,
    BlockingGameSession,
    ExampleSceneManager,
    GenericMenuButton,
    MainMenuScene,
    SimpleRpgBackground,
    SimpleStarsBackground,
    WindowScene
)
from seagulls.examples.rpg import Character, RpgScene
from seagulls.examples.seagulls import SeagullsScene
from seagulls.examples.space_shooter import (
    AsteroidField,
    BlueShip,
    OrangeShip,
    ScoreOverlay,
    ScoreTracker,
    Ship,
    ShipCatalog,
    ShipSelectionMenu,
    ShooterScene,
    SpaceCollisions,
    ActiveShipClient, IShip
)

from ._framework import LoggingClient


class EmptyScene(IGameScene):

    def start(self) -> None:
        raise RuntimeError("You're not supposed to start me.")

    def should_quit(self) -> bool:
        raise RuntimeError("You're not supposed to give me up. Ever.")

    def tick(self) -> None:
        raise RuntimeError("You're not supposed to tick me.")


class EmptyShip(IShip):

    def sprite(self) -> str:
        raise RuntimeError("I have no sprite, I'm empty.")

    def velocity(self) -> int:
        raise RuntimeError("I have no velocity, I'm empty.")

    def power(self) -> int:
        raise RuntimeError("I have no power, I'm empty.")

    def display_name(self) -> str:
        raise RuntimeError("I have no display name, I'm empty.")

    def offset(self) -> int:
        raise RuntimeError("I have no offset, I'm empty.")


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

    _empty_scene = Singleton(
        EmptyScene
    )

    _active_scene_client = Singleton(
        ActiveSceneClient,
        scene=_empty_scene,
    )

    _empty_ship = Singleton(
        EmptyShip
    )

    _active_ship_client = Singleton(
        ActiveShipClient,
        ship=_empty_ship,
    )

    _ship = Singleton(
        Ship,
        active_ship_client=_active_ship_client,
        clock=_game_clock,
        asset_manager=_asset_manager,
        game_controls=_game_controls,
    )

    _asteroid_field = Singleton(
        AsteroidField,
        clock=_game_clock,
        asset_manager=_asset_manager,
    )
    _score_tracker = Singleton(ScoreTracker)

    _score_overlay = Singleton(
        ScoreOverlay,
        score_tracker=_score_tracker,
    )

    _space_collisions = Singleton(
        SpaceCollisions,
        ship=_ship,
        asteroid_field=_asteroid_field,
        rock_collision_callback=_score_tracker.provided.add_point
    )

    _ship_catalog = Singleton(
        ShipCatalog,
        ships=(OrangeShip(), BlueShip()))

    _space_shooter_scene = Singleton(
        ShooterScene,
        clock=_game_clock,
        surface_renderer=_surface_renderer,
        asset_manager=_asset_manager,
        background=_main_menu_background,
        ship=_ship,
        asteroid_field=_asteroid_field,
        space_collisions=_space_collisions,
        score_overlay=_score_overlay,
        game_controls=_game_controls
    )

    _space_shooter_ship_selection_scene = Singleton(
        ShipSelectionMenu,
        catalog=_ship_catalog,
        surface_renderer=_surface_renderer,
        scene=_space_shooter_scene,
        game_controls=_game_controls,
        asset_manager=_asset_manager,
        active_scene_manager=_active_scene_client,
        active_ship_manager=_active_ship_client,
        background=_main_menu_background,
    )

    _space_shooter_menu_button = Singleton(
        GenericMenuButton,
        scene=_space_shooter_ship_selection_scene,
        offset=0,
        button_text="Space Shooter",
        asset_manager=_asset_manager,
        game_controls=_game_controls,
        active_scene_manager=_active_scene_client,
    )

    _seagulls_menu_button = Singleton(
        GenericMenuButton,
        scene=_seagulls_scene,
        offset=80,
        button_text="Seagulls",
        asset_manager=_asset_manager,
        game_controls=_game_controls,
        active_scene_manager=_active_scene_client,
    )

    _rpg_menu_button = Singleton(
        GenericMenuButton,
        scene=_rpg_scene,
        offset=160,
        button_text="RPG",
        asset_manager=_asset_manager,
        game_controls=_game_controls,
        active_scene_manager=_active_scene_client,
    )

    _main_menu_scene = Singleton(
        MainMenuScene,
        surface_renderer=_surface_renderer,
        asset_manager=_asset_manager,
        background=_main_menu_background,
        game_controls=_game_controls,
        space_shooter_menu_button=_space_shooter_menu_button,
        seagulls_menu_button=_seagulls_menu_button,
        rpg_menu_button=_rpg_menu_button,
    )

    _window_scene = Singleton(
        WindowScene,
        active_scene_provider=_active_scene_client,
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
        active_scene_manager=_active_scene_client,
        main_menu_scene=_main_menu_scene,
        space_shooter_scene=_space_shooter_ship_selection_scene,
        seagulls_scene=_seagulls_scene,
        rpg_scene=_rpg_scene,
    )

    example_command = Singleton(ExampleCommand)
