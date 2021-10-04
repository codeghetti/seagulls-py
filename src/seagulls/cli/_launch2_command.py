import logging
import time
from abc import abstractmethod, ABC
from argparse import ArgumentParser
from enum import Enum, auto
from functools import lru_cache
from pathlib import Path
from random import random
from threading import Thread, Event
from pygame.event import Event as PyGameEvent
from typing import Dict, Any, Tuple, List, Callable

import pygame
from pygame.image import load
from pygame.time import Clock
from pygame.transform import flip
from seagulls.engine import Surface, Vector2, Rect

from ._framework import CliCommand

logger = logging.getLogger(__name__)


class GameObject(ABC):

    @abstractmethod
    def tick(self) -> None:
        pass

    @abstractmethod
    def render(self, surface: Surface) -> None:
        pass


class AssetManager:
    _assets_path: Path

    def __init__(self) -> None:
        self._assets_path = Path("assets")

    def load_sprite(self, name: str) -> Surface:
        path = self._assets_path / f"sprites/{name}.png"
        loaded_sprite = load(path.resolve())
        if loaded_sprite.get_alpha() is None:
            return loaded_sprite.convert()
        else:
            return loaded_sprite.convert_alpha()


class SurfaceRenderer:
    def start(self) -> None:
        self._get_surface()

    def render(self, surface: Surface) -> None:
        self._get_surface().blit(surface, (0, 0))
        pygame.display.flip()

    @lru_cache
    def _get_surface(self) -> Surface:
        return pygame.display.set_mode((1024, 600))


class GameClock(GameObject):
    _clock: Clock
    _ticks: int
    _delta: int

    def __init__(self):
        self._clock = Clock()
        self._ticks = 0
        self._delta = 0

    def tick(self) -> None:
        self._delta = self._clock.tick()

    def render(self, surface: Surface) -> None:
        pass

    def get_time(self) -> int:
        return self._delta

    def get_fps(self) -> float:
        return self._clock.get_fps()


class GameControls(GameObject):

    _events: List[PyGameEvent]

    def __init__(self):
        self._events = []

    def tick(self):
        self._events = pygame.event.get()

    def should_quit(self) -> bool:
        for event in self._events:
            if event.type == pygame.QUIT:
                return True

            if self._is_key_down_event(event, pygame.K_ESCAPE):
                return True

        return False

    def should_fire(self) -> bool:
        for event in self._events:
            if self._is_key_down_event(event, pygame.K_SPACE):
                return True

        return False

    def is_left_moving(self) -> bool:
        return pygame.key.get_pressed()[pygame.K_LEFT]

    def is_right_moving(self) -> bool:
        return pygame.key.get_pressed()[pygame.K_RIGHT]

    def should_toggle_debug_hud(self) -> bool:
        for event in self._events:
            if self._is_key_down_event(event, pygame.K_BACKQUOTE):
                return True

        return False

    def _is_key_down_event(self, event: PyGameEvent, key: int) -> bool:
        return event.type == pygame.KEYDOWN and event.key == key

    def _is_key_up_event(self, event: PyGameEvent, key: int) -> bool:
        return event.type == pygame.KEYUP and event.key == key

    def render(self, surface: Surface) -> None:
        pass


class Bird(GameObject):

    _clock: GameClock
    _asset_manager: AssetManager
    _game_controls: GameControls
    _size: Vector2
    _position: Vector2
    _velocity: Vector2

    def __init__(
            self,
            clock: GameClock,
            asset_manager: AssetManager,
            game_controls: GameControls):
        self._clock = clock
        self._asset_manager = asset_manager
        self._game_controls = game_controls

        self._size = Vector2(64, 64)
        # This is the starting position for new wizards
        self._position = Vector2(500, 40)
        self._velocity = Vector2(0, 0)

    def tick(self) -> None:
        if self._game_controls.should_fire():
            logger.info("POOPING")

        if self._game_controls.is_left_moving():
            logger.info("MOVE LEFT")
            self._velocity = Vector2(-1, 0)
        elif self._game_controls.is_right_moving():
            logger.info("MOVE RIGHT")
            self._velocity = Vector2(1, 0)
        else:
            self._velocity = Vector2(0, 0)

        delta = self._clock.get_time()

        self._position = self._position + (self._velocity * delta / 10)

        if self._position.x < 30:
            self._position.x = 30

        if self._position.x > 995:
            self._position.x = 995

    def render(self, surface: Surface) -> None:
        sprite = self._get_sprite().copy().convert_alpha()
        radius = self._size.x / 2
        blit_position = self._position - Vector2(radius)

        if self._game_controls.is_left_moving():
            sprite = flip(sprite, True, False)

        surface.blit(sprite, (blit_position.x, blit_position.y))

    def _get_sprite(self) -> Surface:
        sprite_sheet = self._get_sprite_sheet()
        rect = Rect((64 * 0, 0), (64, 64))

        result = Surface(rect.size)
        result.blit(sprite_sheet, (0, 0), rect)

        # Not really sure why this is needed but meh. Losing transparency if I don't do this.
        colorkey = result.get_at((0, 0))
        result.set_colorkey(colorkey, pygame.RLEACCEL)

        return flip(result.convert_alpha(), True, False)

    @lru_cache()
    def _get_sprite_sheet(self) -> Surface:
        return self._asset_manager.load_sprite("seagull/seagull-walking")

    def is_destroyed(self) -> bool:
        return False


class Background(GameObject):

    _asset_manager: AssetManager

    def __init__(
            self,
            asset_manager: AssetManager):
        self._asset_manager = asset_manager

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        background = self._get_cached_background()
        surface.blit(background, (0, 0))

    @lru_cache()
    def _get_cached_background(self) -> Surface:
        background = self._asset_manager.load_sprite("environment/environment-sky").copy()

        things = [
            # These need to be in the order they should be rendered on top of the sky
            self._asset_manager.load_sprite("environment/environment-stars"),
            self._asset_manager.load_sprite("environment/environment-wall"),
            self._asset_manager.load_sprite("environment/environment-bookshelves"),
            self._asset_manager.load_sprite("environment/environment-ladders"),
            self._asset_manager.load_sprite("environment/environment-floor"),
            self._asset_manager.load_sprite("environment/environment-rampart"),
            self._asset_manager.load_sprite("environment/environment-perch"),
            self._asset_manager.load_sprite("environment/environment-scrolls"),
            self._asset_manager.load_sprite("environment/environment-spider"),
        ]

        for thing in things:
            background.blit(thing, (0, 0))

        return background


class GameObjectsCollection:
    _game_objects: List[GameObject]

    def __init__(self) -> None:
        self._game_objects = []

    def add(self, game_object: GameObject) -> None:
        self._game_objects.append(game_object)

    def apply(self, func: Callable[[GameObject], None]) -> None:
        for game_object in self._game_objects:
            func(game_object)


class WizardState(Enum):
    STANDING = auto()
    WALKING = auto()
    ATTACKING = auto()


class SimpleWizard(GameObject):

    _clock: GameClock
    _scene_objects: GameObjectsCollection
    # _fireball_factory: WizardFireballFactory
    _asset_manager: AssetManager
    _sprite: Surface

    _size: Vector2
    _position: Vector2
    _velocity: Vector2
    _current_state: WizardState
    _current_state_duration: int  # time we have spent since switching to this state

    def __init__(
            self,
            clock: GameClock,
            scene_objects: GameObjectsCollection,
            # fireball_factory: WizardFireballFactory,
            asset_manager: AssetManager):
        self._clock = clock
        self._scene_objects = scene_objects
        # self._fireball_factory = fireball_factory
        self._asset_manager = asset_manager

        self._size = Vector2(64, 64)
        # This is the starting position for new wizards
        self._position = Vector2(0, 518)
        self._velocity = Vector2(1, 0)
        self._current_state = WizardState.WALKING
        self._current_state_duration = 0

    def tick(self) -> None:
        # A bit hacky but we flip the direction the wizard is moving
        # When ever they get close to the edges of the screen
        if self._position.x > 1015:
            self._velocity = Vector2(-1, 0)
        elif self._position.x < 10:
            self._velocity = Vector2(1, 0)

        # if self._should_fire():
        #     self._attack()

        delta = self._clock.get_time()
        self._current_state_duration += delta

        # if self._current_state == WizardState.ATTACKING:
        #     if self._current_state_duration > 2000:
        #         fireball = self._fireball_factory.create(self._position)
        #         self._scene_manager.get_scene_objects().add(fireball)
        #         self._walk()

        self._position = self._position + (self._velocity * delta / 10)

    def _should_fire(self) -> bool:
        if self._current_state == WizardState.ATTACKING:
            return False

        rnd = random() * 1000
        return self._current_state_duration / 1000 > rnd

    def _attack(self) -> None:
        if self._current_state == WizardState.ATTACKING:
            return

        self._set_state(WizardState.ATTACKING)
        self._velocity = Vector2(0, 0)

    def _walk(self) -> None:
        if self._current_state == WizardState.WALKING:
            return

        self._set_state(WizardState.WALKING)
        self._velocity = Vector2(1, 0)

    def _set_state(self, state: WizardState) -> None:
        self._current_state = state
        self._current_state_duration = 0

    def render(self, surface: Surface) -> None:
        sprite = self._get_sprite().copy().convert_alpha()
        radius = self._size.x / 2
        blit_position = self._position - Vector2(radius)
        surface.blit(sprite, (blit_position.x, blit_position.y))

    def _get_sprite(self) -> Surface:
        frames = {
            WizardState.WALKING: self._walking_frames(),
            WizardState.ATTACKING: self._attacking_frames(),
            WizardState.STANDING: self._standing_frames(),
        }[self._current_state]

        current_walking_frame = (self._current_state_duration / 300) % len(frames)
        return frames[int(current_walking_frame)]

    @lru_cache()
    def _walking_frames(self) -> List[Surface]:
        return [
            self._sprite_sheet_slice(Rect((64 * 0, 0), (64, 64))),
            self._sprite_sheet_slice(Rect((64 * 1, 0), (64, 64))),
        ]

    @lru_cache()
    def _attacking_frames(self) -> List[Surface]:
        return [
            self._sprite_sheet_slice(Rect((64 * 2, 0), (64, 64))),
            self._sprite_sheet_slice(Rect((64 * 3, 0), (64, 64))),
            self._sprite_sheet_slice(Rect((64 * 4, 0), (64, 64))),
        ]

    @lru_cache()
    def _standing_frames(self) -> List[Surface]:
        return [
            self._sprite_sheet_slice(Rect((64 * 0, 0), (64, 64))),
            self._sprite_sheet_slice(Rect((64 * 2, 0), (64, 64))),
        ]

    def _sprite_sheet_slice(self, rect: Rect) -> Surface:
        sprite_sheet = self._get_sprite_sheet()

        result = Surface(rect.size)
        result.blit(sprite_sheet, (0, 0), rect)

        # Not really sure why this is needed but meh. Losing transparency if I don't do this.
        colorkey = result.get_at((0, 0))
        result.set_colorkey(colorkey, pygame.RLEACCEL)

        return result.convert_alpha()

    @lru_cache()
    def _get_sprite_sheet(self) -> Surface:
        return self._asset_manager.load_sprite("wizard/wizard1-spritesheet")

    def is_destroyed(self) -> bool:
        return False


class GameScene:

    _name: str
    __asset_manager: AssetManager
    _surface_renderer: SurfaceRenderer
    _game_controls = GameControls
    _game_objects: GameObjectsCollection
    _should_quit: Event

    def __init__(self, name: str) -> None:
        self._name = name
        self._surface_renderer = SurfaceRenderer()
        self._asset_manager = AssetManager()

        clock = GameClock()

        self._game_controls = GameControls()
        self._should_quit = Event()

        background = Background(asset_manager=self._asset_manager)

        bird = Bird(
            clock=clock,
            asset_manager=self._asset_manager,
            game_controls=self._game_controls,
        )

        self._game_objects = GameObjectsCollection()

        wizard = SimpleWizard(
            clock=clock,
            scene_objects=self._game_objects,
            asset_manager=self._asset_manager)

        self._game_objects.add(clock)
        self._game_objects.add(self._game_controls)
        self._game_objects.add(background)
        self._game_objects.add(bird)
        self._game_objects.add(wizard)

    def start(self) -> None:
        self._surface_renderer.start()
        self.tick()

    def should_quit(self) -> bool:
        return self._game_controls.should_quit()

    def tick(self) -> None:
        self._game_objects.apply(lambda x: x.tick())

        if self._game_controls.should_quit():
            self._should_quit.set()

        self._render()

    def _render(self) -> None:
        background = Surface((1024, 600))
        self._game_objects.apply(lambda x: x.render(background))

        self._surface_renderer.render(background)


class GameSceneManager:
    def get_scene(self, name: str) -> GameScene:
        return GameScene(name)


class GameSession:

    _name: str
    _game_scene_manager: GameSceneManager
    _thread: Thread
    _stopped: Event

    def __init__(self, name: str) -> None:
        self._name = name
        self._game_scene_manager = GameSceneManager()
        self._thread = Thread(target=self._thread_target)
        self._stopped = Event()

    def start(self) -> None:
        logger.debug(f"starting game session {self._name}")
        self._thread.start()

    def wait_for_completion(self) -> None:
        logger.debug(f"waiting for completion {self._name}")
        while not self._stopped.is_set():
            time.sleep(0.2)
        logger.debug(f"done waiting for completion {self._name}")

    def stop(self) -> None:
        logger.debug(f"stopping game session {self._name}")
        self._stopped.set()
        self._thread.join()

    def _thread_target(self) -> None:
        pygame.display.set_caption("Our Game")
        scene = self._game_scene_manager.get_scene(self._name)
        scene.start()

        while not self._stopped.is_set() and not scene.should_quit():
            scene.tick()
        logger.debug("exiting game session")
        self._stopped.set()


class GameManager:

    def get_session(self, scene: str) -> GameSession:
        return GameSession(scene)


class Launch2Command(CliCommand):

    _game_manager: GameManager

    def __init__(self, game_manager: GameManager):
        self._game_manager = game_manager

    def get_command_name(self) -> str:
        return "launch2"

    def get_command_help(self) -> str:
        return "Launch the seagulls game."

    def configure_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("scene", help="Set upper bound FPS limit")

    def execute(self, args: Dict[str, Any]):
        session = self._game_manager.get_session(args["scene"])

        try:
            session.start()
            session.wait_for_completion()
        except KeyboardInterrupt:
            session.stop()
