import logging
from functools import lru_cache
from threading import Event

import pygame
from pygame import Surface, mixer
from seagulls.assets import AssetManager
from seagulls.engine import (
    GameControls,
    GameObject,
    GameObjectsCollection,
    IGameScene,
    ISetActiveScene,
    SurfaceRenderer
)

from ._game_over_overlay import GameOverOverlay
from ._replay_shooter_button import ReplayShooterButton
from ._score_overlay import ScoreOverlay

logger = logging.getLogger(__name__)


class GameOverScene(IGameScene):
    _surface_renderer: SurfaceRenderer

    _game_controls: GameControls
    _asset_manager: AssetManager
    _active_scene_manager: ISetActiveScene

    _game_objects: GameObjectsCollection
    _should_quit: Event

    _score_overlay: ScoreOverlay

    def __init__(
            self,
            replay_button: ReplayShooterButton,
            surface_renderer: SurfaceRenderer,
            game_controls: GameControls,
            asset_manager: AssetManager,
            active_scene_manager: ISetActiveScene,
            score_overlay: ScoreOverlay,
            background: GameObject):
        self._replay_button = replay_button
        self._surface_renderer = surface_renderer
        self._game_controls = game_controls
        self._asset_manager = asset_manager
        self._active_scene_manager = active_scene_manager

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(background)
        self._game_objects.add(score_overlay)
        self._game_objects.add(self._game_controls)
        self._game_objects.add(self._replay_button)

        self._score_overlay = score_overlay
        self._should_quit = Event()

    def start(self) -> None:
        self._surface_renderer.start()
        self.tick()

    def should_quit(self) -> bool:
        return self._should_quit.is_set()

    def tick(self) -> None:
        self._game_objects.apply(lambda x: x.tick())

        if self._game_controls.should_quit():
            logger.debug("QUIT EVENT DETECTED")
            self._should_quit.set()

        self._game_over_summary()

        self._render()

    @lru_cache()
    def _game_over_summary(self) -> None:
        mixer.init()
        mixer.Sound("assets/sounds/game-over.ogg").play()
        self._game_objects.add(GameOverOverlay())

    def _render(self) -> None:
        background = Surface((self._get_display_width(), self._get_display_height()))
        self._game_objects.apply(lambda x: x.render(background))

        self._surface_renderer.render(background)

    @lru_cache()
    def _get_display_width(self) -> int:
        return pygame.display.Info().current_w

    @lru_cache()
    def _get_display_height(self) -> int:
        return pygame.display.Info().current_h


class GameOverSceneFactory:
    _surface_renderer: SurfaceRenderer
    _game_controls: GameControls
    _asset_manager: AssetManager
    _active_scene_manager: ISetActiveScene
    _score_overlay: ScoreOverlay
    _background: GameObject

    def __init__(
            self,
            surface_renderer: SurfaceRenderer,
            game_controls: GameControls,
            asset_manager: AssetManager,
            active_scene_manager: ISetActiveScene,
            score_overlay: ScoreOverlay,
            background: GameObject):
        self._surface_renderer = surface_renderer
        self._game_controls = game_controls
        self._asset_manager = asset_manager
        self._active_scene_manager = active_scene_manager
        self._score_overlay = score_overlay
        self._background = background

    def get_instance(self, replay_button: ReplayShooterButton) -> GameOverScene:
        return GameOverScene(
            replay_button,
            self._surface_renderer,
            self._game_controls,
            self._asset_manager,
            self._active_scene_manager,
            self._score_overlay,
            self._background
        )
