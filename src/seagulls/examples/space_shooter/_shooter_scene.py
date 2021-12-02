import logging
from abc import abstractmethod, ABC
from enum import Enum, auto
from functools import lru_cache
from pathlib import Path
from threading import Event
from typing import Tuple

from pygame import mixer
from pygame.font import Font

from seagulls.assets import AssetManager
from seagulls.engine import (
    GameClock,
    GameControls,
    GameObject,
    GameObjectsCollection,
    IGameScene,
    Surface,
    SurfaceRenderer
)
from ._asteroid_field import AsteroidField
from ._ship import Ship

logger = logging.getLogger(__name__)


class ShooterSceneState(Enum):
    RUNNING = auto()
    WON = auto()
    LOST = auto()


class ShooterSceneStateClient:
    _current_state: ShooterSceneState

    def __init__(self):
        self._current_state = ShooterSceneState.RUNNING

    def update_state(self, state: ShooterSceneState) -> None:
        self._current_state = state

    def get_state(self) -> ShooterSceneState:
        return self._current_state


class ICheckGameRules(ABC):

    @abstractmethod
    def check(self) -> None:
        pass


class AsteroidMissedRule(ICheckGameRules):
    _state_client: ShooterSceneStateClient
    _asteroid_field: AsteroidField

    def __init__(self, state_client: ShooterSceneStateClient, asteroid_field: AsteroidField):
        self._state_client = state_client
        self._asteroid_field = asteroid_field

    def check(self) -> None:
        for x in range(self._asteroid_field.get_asteroid_field_size()):
            if self._asteroid_field.get_rock_position_y(x) > 600:
                self._state_client.update_state(ShooterSceneState.LOST)


class ShipDestroyedRule(ICheckGameRules):
    _state_client: ShooterSceneStateClient
    _asteroid_field: AsteroidField
    _ship: Ship

    def __init__(
            self,
            state_client: ShooterSceneStateClient,
            asteroid_field: AsteroidField,
            ship: Ship):
        self._state_client = state_client
        self._asteroid_field = asteroid_field
        self._ship = ship

    def check(self) -> None:
        for index in range(self._asteroid_field.get_asteroid_field_size()):
            if self._ship_rock_collision_check(index):
                self._state_client.update_state(ShooterSceneState.LOST)
                return

    def _ship_rock_collision_check(self, rock_number: int) -> bool:
        ship_position = self._ship.get_ship_position()

        nose_collision_check = (
            self._asteroid_field.get_rock_position_x(rock_number) <= (ship_position.x + 50) <=
            self._asteroid_field.get_rock_position_x(rock_number) +
            self._asteroid_field.get_rock_size_x(rock_number) and
            self._asteroid_field.get_rock_position_y(rock_number) <=
            ship_position.y <=
            self._asteroid_field.get_rock_position_y(rock_number) +
            self._asteroid_field.get_rock_size_y(rock_number)
        )

        left_upper_wing_check = (
            self._asteroid_field.get_rock_position_x(rock_number) <= ship_position.x <=
            self._asteroid_field.get_rock_position_x(rock_number) +
            self._asteroid_field.get_rock_size_x(rock_number) and
            self._asteroid_field.get_rock_position_y(rock_number) <=
            (ship_position.y + 30) <=
            self._asteroid_field.get_rock_position_y(rock_number) +
            self._asteroid_field.get_rock_size_y(rock_number)
        )

        right_upper_wing_check = (
            self._asteroid_field.get_rock_position_x(rock_number) <= (ship_position.x + 105) <=
            self._asteroid_field.get_rock_position_x(rock_number) +
            self._asteroid_field.get_rock_size_x(rock_number) and
            self._asteroid_field.get_rock_position_y(rock_number) <=
            (ship_position.y + 30) <=
            self._asteroid_field.get_rock_position_y(rock_number) +
            self._asteroid_field.get_rock_size_y(rock_number)
        )

        left_lower_wing_check = (
            self._asteroid_field.get_rock_position_x(rock_number) <= ship_position.x <=
            self._asteroid_field.get_rock_position_x(rock_number) +
            self._asteroid_field.get_rock_size_x(rock_number)
            and self._asteroid_field.get_rock_position_y(rock_number) <=
            (ship_position.y + 68) <=
            self._asteroid_field.get_rock_position_y(rock_number) +
            self._asteroid_field.get_rock_size_y(rock_number)
        )

        right_lower_wing_check = (
            self._asteroid_field.get_rock_position_x(rock_number) <= (ship_position.x + 105) <=
            self._asteroid_field.get_rock_position_x(rock_number) +
            self._asteroid_field.get_rock_size_x(rock_number) and
            self._asteroid_field.get_rock_position_y(rock_number) <=
            (ship_position.y + 68) <=
            self._asteroid_field.get_rock_position_y(rock_number) +
            self._asteroid_field.get_rock_size_y(rock_number)
        )

        return (
            nose_collision_check or
            left_lower_wing_check or
            right_lower_wing_check or
            left_upper_wing_check or
            right_upper_wing_check)


class GameOverOverlay(GameObject):

    _font: Font

    def __init__(self):
        self._font = Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 50)

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        img = self._font.render(
            "GAME OVER",
            True,
            "red", "black"
        )
        surface.blit(img, (380, 260))


class ScoreTracker:

    def __init__(self):
        self._score = 0

    def add_point(self) -> None:
        self._score += 1

    def get_score(self) -> int:
        return self._score


class ScoreOverlay(GameObject):

    _font: Font

    def __init__(
            self,
            score_tracker: ScoreTracker):

        self._font = Font(Path("assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 18)
        self._score_tracker = score_tracker

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        img = self._font.render(
            f"Score: {self._score_tracker.get_score()}",
            True,
            "red", "black"
        )
        surface.blit(img, (920, 570))


class ToggleableGameObject(GameObject):
    _game_object: GameObject
    _active: bool

    def __init__(self, game_object: GameObject):
        self._game_object = game_object
        self._active = True

    def tick(self) -> None:
        if self._active:
            self._game_object.tick()

    def render(self, surface: Surface) -> None:
        if self._active:
            self._game_object.render(surface)

    def toggle(self) -> None:
        self._active = not self._active


class ShooterScene(IGameScene):

    _surface_renderer: SurfaceRenderer
    _game_controls: GameControls
    _asset_manager: AssetManager

    _game_objects: GameObjectsCollection
    _should_quit: Event

    _state_client: ShooterSceneStateClient
    _game_rules: Tuple[ICheckGameRules, ...]

    _toggleables: Tuple[ToggleableGameObject, ...]

    def __init__(
            self,
            clock: GameClock,
            surface_renderer: SurfaceRenderer,
            asset_manager: AssetManager,
            background: GameObject,
            ship: Ship,
            asteroid_field: AsteroidField,
            space_collisions: GameObject,
            score_overlay: ScoreOverlay,
            game_controls: GameControls):
        mixer.init()
        self._surface_renderer = surface_renderer
        self._asset_manager = asset_manager
        self._game_controls = game_controls

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(clock)
        self._game_objects.add(background)
        self._game_objects.add(ship)
        self._game_objects.add(space_collisions)
        self._game_objects.add(score_overlay)
        self._game_objects.add(self._game_controls)

        self._toggleables = tuple([
            ToggleableGameObject(asteroid_field)
        ])

        self._state_client = ShooterSceneStateClient()
        self._game_rules = tuple([
            AsteroidMissedRule(self._state_client, asteroid_field),
            ShipDestroyedRule(self._state_client, asteroid_field, ship),
        ])

        for item in self._toggleables:
            self._game_objects.add(item)

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

        for rule in self._game_rules:
            rule.check()

        if not self._state_client.get_state() == ShooterSceneState.RUNNING:
            self._end_game()

        self._render()

    @lru_cache()
    def _end_game(self) -> None:
        mixer.Sound("assets/sounds/game-over.ogg").play()
        self._game_objects.add(GameOverOverlay())
        for item in self._toggleables:
            item.toggle()

    def _render(self) -> None:
        background = Surface((1024, 600))
        self._game_objects.apply(lambda x: x.render(background))

        self._surface_renderer.render(background)
