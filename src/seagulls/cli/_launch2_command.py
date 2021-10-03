import logging
import time
from abc import abstractmethod, ABC
from argparse import ArgumentParser
from functools import lru_cache
from pathlib import Path
from threading import Thread, Event
from pygame.event import Event as PyGameEvent
from typing import Dict, Any, Tuple, List

import pygame
from pygame.image import load
from pygame.time import Clock
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
        surface.blit(sprite, (blit_position.x, blit_position.y))

    def _get_sprite(self) -> Surface:
        sprite_sheet = self._get_sprite_sheet()
        rect = Rect((64 * 0, 0), (64, 64))

        result = Surface(rect.size)
        result.blit(sprite_sheet, (0, 0), rect)

        # Not really sure why this is needed but meh. Losing transparency if I don't do this.
        colorkey = result.get_at((0, 0))
        result.set_colorkey(colorkey, pygame.RLEACCEL)

        return result.convert_alpha()

    @lru_cache()
    def _get_sprite_sheet(self) -> Surface:
        return self._asset_manager.load_sprite("seagull/seagull-walking")

    def is_destroyed(self) -> bool:
        return False


class GameScene:

    _name: str
    __asset_manager: AssetManager
    _surface_renderer: SurfaceRenderer
    _game_controls = GameControls
    _game_objects: Tuple[GameObject, ...]
    _should_quit: Event

    def __init__(self, name: str) -> None:
        self._name = name
        self._surface_renderer = SurfaceRenderer()
        self._asset_manager = AssetManager()

        clock = GameClock()
        self._game_controls = GameControls()
        self._should_quit = Event()

        self._game_objects = tuple([
            clock,
            self._game_controls,
            Bird(
                clock=clock,
                asset_manager=self._asset_manager,
                game_controls=self._game_controls,
            ),
        ])

    def start(self) -> None:
        self._surface_renderer.start()
        self.tick()

    def should_quit(self) -> bool:
        return self._game_controls.should_quit()

    def tick(self) -> None:
        for game_object in self._game_objects:
            game_object.tick()

        if self._game_controls.should_quit():
            self._should_quit.set()

        self._render()

    def _render(self) -> None:
        background = self._asset_manager.load_sprite("environment/environment-sky").copy()
        for game_object in self._game_objects:
            game_object.render(background)

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
