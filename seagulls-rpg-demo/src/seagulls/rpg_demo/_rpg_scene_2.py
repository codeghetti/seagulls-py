import logging

import pygame
from seagulls.engine import GameClock, GameControls
from seagulls.pygame import WindowSurface
from seagulls.rendering import (
    Camera,
    IPrinter,
    Position,
    SpriteClient,
    SpritesType
)
from seagulls.scene import IGameScene, IProvideGameScenes
from seagulls.session import IProvideGameSessions

logger = logging.getLogger(__name__)


class Sprites(SpritesType):
    floor_left_corner = "floor-left-corner"
    floor_middle = "floor-middle"
    floor_right_corner = "floor-right-corner"
    pumpkin = "pumpkin"
    dead_pumpkin = "dead-pumpkin"
    ghost = "ghost"
    sword = "sword"


class RpgScene2(IGameScene):

    _session: IProvideGameSessions
    _printer: IPrinter
    _camera: Camera

    def __init__(
            self,
            session: IProvideGameSessions,
            printer: IPrinter,
            window: WindowSurface,
            camera: Camera,
            sprite_client: SpriteClient,
            game_controls: GameControls,
            clock: GameClock):
        self._session = session
        self._printer = printer
        self._window = window
        self._camera = camera
        self._sprite_client = sprite_client
        self._game_controls = game_controls
        self._clock = clock
        self._pumpkin_position = 10
        self._ghost_position = 400
        self._ghost_moves_right = True
        self._is_sword_out = False
        self._is_game_over = False

    def tick(self) -> None:
        self._printer.clear()
        self._game_controls.tick()
        self._clock.tick()
        delta = self._clock.get_time()

        self.make_floor()
        self.walking_ghost(delta)

        if self._is_game_over:
            self._sprite_client.render_sprite(
                Sprites.dead_pumpkin,
                Position({"x": self._pumpkin_position, "y": 515})
            )

        if not self._is_game_over:
            self.pumpkin_movement(delta)

            self._sprite_client.render_sprite(
                Sprites.pumpkin,
                Position({"x": self._pumpkin_position, "y": 515})
            )

            if self._game_controls.should_fire():
                self._is_sword_out = not self._is_sword_out

            if self._is_sword_out:
                self._sprite_client.render_sprite(
                    Sprites.sword,
                    Position({"x": self._pumpkin_position + 25, "y": 515})
                )

            pumpkin_rect = pygame.Rect((self._pumpkin_position, 515), (35, 35))
            ghost_rect = pygame.Rect((self._ghost_position, 500), (50, 50))
            collision = pygame.Rect.colliderect(pumpkin_rect, ghost_rect)

            if collision:
                self._is_game_over = True

        self._printer.commit()

    def pumpkin_movement(self, delta):
        if self._game_controls.is_right_moving() and self._pumpkin_position <= 955:
            self._pumpkin_position += int(10 * delta / 25)

        elif self._game_controls.is_left_moving() and self._pumpkin_position > 5:
            self._pumpkin_position -= int(10 * delta / 25)

    def walking_ghost(self, delta):
        if self._ghost_moves_right:
            new_position = self._ghost_position + int(5 * delta / 25)
            self._ghost_position = new_position if new_position <= 800 else 800
        if not self._ghost_moves_right:
            new_position = self._ghost_position - int(5 * delta / 25)
            self._ghost_position = new_position if new_position >= 400 else 400
        if self._ghost_position == 400 or self._ghost_position == 800:
            self._ghost_moves_right = not self._ghost_moves_right
        self._sprite_client.render_sprite(
            Sprites.ghost,
            Position({"x": self._ghost_position, "y": 500})
        )

    def make_floor(self):
        self._sprite_client.render_sprite(
            Sprites.floor_left_corner,
            Position({"x": 0, "y": 550})
        )

        for x in range(int(900 / 50)):
            self._sprite_client.render_sprite(
                Sprites.floor_middle,
                Position({"x": 50 + x * 50, "y": 550})
            )

        self._sprite_client.render_sprite(
            Sprites.floor_right_corner,
            Position({"x": 950, "y": 550})
        )


class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene
