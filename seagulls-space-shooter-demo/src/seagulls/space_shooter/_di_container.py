from functools import lru_cache
from pathlib import Path

from seagulls.assets import AssetManager
from seagulls.engine import (
    ActiveSceneClient,
    BasicSceneManager,
    BlockingGameSession,
    EmptyScene,
    GameClock,
    GameControls,
    SurfaceRenderer,
    WindowScene
)
from seagulls.seagulls_cli import SeagullsCliApplication

from ._active_ship_client import ActiveShipClient
from ._asteroid_field import AsteroidField
from ._blue_ship import BlueShip
from ._cli_command import GameCliCommand
from ._cli_plugin import SpaceShooterCliPlugin
from ._empty_ship import EmptyShip
from ._fit_to_screen import FitToScreen
from ._game_over_scene import GameOverSceneFactory
from ._orange_ship import OrangeShip
from ._replay_shooter_button import ReplayButtonFactory
from ._score_overlay import ScoreOverlay
from ._score_tracker import ScoreTracker
from ._selectable_ship_menu import ShipSelectionMenuFactory
from ._ship import Ship
from ._ship_catalog import ShipCatalog
from ._shooter_scene import ShooterScene
from ._space_collisions import SpaceCollisions
from ._stars_background import SimpleStarsBackground


class SpaceShooterDiContainer:
    _application: SeagullsCliApplication

    def __init__(self, application: SeagullsCliApplication):
        self._application = application

    @lru_cache()
    def plugin(self) -> SpaceShooterCliPlugin:
        return SpaceShooterCliPlugin(application=self._application, command=self._command())

    @lru_cache()
    def _command(self) -> GameCliCommand:
        return GameCliCommand(
            game_session=self._blocking_game_session(),
            active_scene_manager=self._active_scene_client(),
            ship_selection_scene_factory=self._ship_selection_menu_factory(),
            space_shooter_scene=self._scene())

    @lru_cache()
    def _blocking_game_session(self) -> BlockingGameSession:
        return BlockingGameSession(
            scene_manager=BasicSceneManager(scene=self._window_scene()))

    @lru_cache()
    def _window_scene(self) -> WindowScene:
        return WindowScene(
            active_scene_provider=self._active_scene_client(),
        )

    @lru_cache()
    def _scene(self) -> ShooterScene:
        return ShooterScene(
            clock=self._game_clock(),
            surface_renderer=self._surface_renderer(),
            asset_manager=self._asset_manager(),
            active_scene_manager=self._active_scene_client(),
            background=self._main_menu_background(),
            ship=self._ship(),
            asteroid_field=self._asteroid_field(),
            space_collisions=self._space_collisions(),
            score_overlay=self._score_overlay(),
            game_controls=self._game_controls(),
            game_over_scene_factory=self._game_over_scene_factory(),
            replay_button_factory=self._replay_button_factory(),
            ship_selection_menu_factory=self._ship_selection_menu_factory(),
            fit_to_screen=self._fit_to_screen()
        )

    @lru_cache()
    def _ship_selection_menu_factory(self) -> ShipSelectionMenuFactory:
        return ShipSelectionMenuFactory(
            catalog=self._ship_catalog(),
            surface_renderer=self._surface_renderer(),
            game_controls=self._game_controls(),
            asset_manager=self._asset_manager(),
            active_scene_manager=self._active_scene_client(),
            active_ship_manager=self._active_ship_client(),
            background=self._main_menu_background(),
            fit_to_screen=self._fit_to_screen()
        )

    @lru_cache()
    def _ship_catalog(self) -> ShipCatalog:
        return ShipCatalog(
            ships=(OrangeShip(), BlueShip(self._fit_to_screen())))

    @lru_cache()
    def _replay_button_factory(self) -> ReplayButtonFactory:
        return ReplayButtonFactory(
            asset_manager=self._asset_manager(),
            game_controls=self._game_controls(),
            active_scene_manager=self._active_scene_client(),
            fit_to_screen=self._fit_to_screen()
        )

    @lru_cache()
    def _game_over_scene_factory(self) -> GameOverSceneFactory:
        return GameOverSceneFactory(
            surface_renderer=self._surface_renderer(),
            game_controls=self._game_controls(),
            asset_manager=self._asset_manager(),
            active_scene_manager=self._active_scene_client(),
            score_overlay=self._score_overlay(),
            background=self._main_menu_background(),
            fit_to_screen=self._fit_to_screen()
        )

    @lru_cache()
    def _space_collisions(self) -> SpaceCollisions:
        return SpaceCollisions(
            ship=self._ship(),
            asteroid_field=self._asteroid_field(),
            rock_collision_callback=self._score_tracker().add_point)

    @lru_cache()
    def _score_overlay(self) -> ScoreOverlay:
        return ScoreOverlay(
            score_tracker=self._score_tracker(),
            fit_to_screen=self._fit_to_screen())

    @lru_cache()
    def _score_tracker(self) -> ScoreTracker:
        return ScoreTracker()

    @lru_cache()
    def _asteroid_field(self) -> AsteroidField:
        return AsteroidField(
            clock=self._game_clock(),
            asset_manager=self._asset_manager(),
            fit_to_screen=self._fit_to_screen()
        )

    @lru_cache()
    def _ship(self) -> Ship:
        return Ship(
            active_ship_manager=self._active_ship_client(),
            clock=self._game_clock(),
            asset_manager=self._asset_manager(),
            game_controls=self._game_controls(),
            fit_to_screen=self._fit_to_screen()
        )

    @lru_cache()
    def _active_scene_client(self) -> ActiveSceneClient:
        return ActiveSceneClient(scene=self._empty_scene())

    @lru_cache()
    def _active_ship_client(self) -> ActiveShipClient:
        return ActiveShipClient(ship=self._empty_ship())

    @lru_cache()
    def _empty_scene(self) -> EmptyScene:
        return EmptyScene()

    @lru_cache()
    def _empty_ship(self) -> EmptyShip:
        return EmptyShip()

    @lru_cache()
    def _main_menu_background(self) -> SimpleStarsBackground:
        return SimpleStarsBackground(
            asset_manager=self._asset_manager(),
            fit_to_screen=self._fit_to_screen()
        )

    @lru_cache()
    def _fit_to_screen(self) -> FitToScreen:
        return FitToScreen()

    @lru_cache()
    def _surface_renderer(self) -> SurfaceRenderer:
        return SurfaceRenderer()

    @lru_cache()
    def _game_clock(self) -> GameClock:
        return GameClock()

    @lru_cache()
    def _game_controls(self) -> GameControls:
        return GameControls()

    @lru_cache()
    def _asset_manager(self) -> AssetManager:
        return AssetManager(assets_path=Path("assets"))
