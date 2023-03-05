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
    full_health = "full-health"
    half_health = "half-health"
    zero_health = "zero-health"
    game_over = "game-over"
    you_win = "you-win"
    flag_banner = "flag-banner"
    flag_pole = "flag-pole"
    green_ghost = "green-ghost"
    dark_wizard = "dark-wizard"


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
        self._scene_right_limit = 2800
        self._x_pumpkin_position = 10
        self._y_position_pumpkin = 515.0
        self._x_position_flag_banner = self._scene_right_limit - 100
        self._y_position_flag_banner = 450
        self._x_position_flag_pole = self._scene_right_limit - 100
        self._y_position_flag_pole = 500
        self._vertical_velocity = 0.0
        self._ghost_position = 400
        self._green_ghost_position = 1200
        self._ghost_moves_right = True
        self._green_ghost_moves_right = True
        self._is_weapon_out = False
        self._is_jumping = False
        self._is_game_over = False
        self._is_game_won = False
        self._health_points = 2
        self._damage_taken_buffer = 0
        self._weapon_offset = 25
        self._ghost_alive = True
        self._green_ghost_alive = True
        self._x_sword_position = 0
        self._y_position_sword = 0

    def tick(self) -> None:
        self._printer.clear()
        self._game_controls.tick()

        self._clock.tick()
        delta = self._clock.get_time()
        self._damage_taken_buffer += delta

        self.make_floor()
        self.heart_health(self._health_points)

        if self._is_game_won:
            self._sprite_client.render_sprite(
                Sprites.you_win,
                self._camera.relative_position(
                    Position({"x": 225, "y": 225}))
            )

        if self._ghost_alive:
            self.walking_ghost(delta)

        if self._green_ghost_alive:
            self.walking_green_ghost(delta)

        if self._is_game_over:
            self._sprite_client.render_sprite(
                Sprites.dead_pumpkin,
                Position({"x": self._x_pumpkin_position, "y": 515})
            )
            self._sprite_client.render_sprite(
                Sprites.game_over,
                self._camera.relative_position(
                    Position({"x": 225, "y": 225}))
            )
        else:
            self.pumpkin_x_axis_movement(delta)
            self.pumpkin_y_axis_movement(delta)
            self._camera.update_position(Position(
                {"x": self._x_pumpkin_position-100, "y": 0}))

            self._sprite_client.render_sprite(
                Sprites.flag_banner,
                Position({"x": self._x_position_flag_banner, "y": self._y_position_flag_banner})
            )
            self._sprite_client.render_sprite(
                Sprites.flag_pole,
                Position({"x": self._x_position_flag_pole, "y": self._y_position_flag_pole})
            )

            self._sprite_client.render_sprite(
                Sprites.pumpkin,
                Position({"x": self._x_pumpkin_position, "y": int(self._y_position_pumpkin)})
            )

            self.weapon_firing(delta)

            pumpkin_rect = pygame.Rect((self._x_pumpkin_position, self._y_position_pumpkin),
                                       (35, 35))
            ghost_rect = pygame.Rect((self._ghost_position, 500), (50, 50))

            green_ghost_rect = pygame.Rect((self._green_ghost_position, 500), (50, 50))

            sword_rect = pygame.Rect(
                (self._x_sword_position + self._weapon_offset, self._y_position_sword), (35, 35)
            )

            flag_rect = pygame.Rect(
                (self._x_position_flag_banner, self._y_position_flag_banner), (50, 100)
            )

            if pygame.Rect.colliderect(sword_rect, ghost_rect) \
                    and self._ghost_alive \
                    and self._is_weapon_out:
                self._ghost_alive = False

            if pygame.Rect.colliderect(sword_rect, green_ghost_rect) \
                    and self._green_ghost_alive \
                    and self._is_weapon_out:
                self._green_ghost_alive = False

            if (
                    pygame.Rect.colliderect(pumpkin_rect, ghost_rect)
                    or pygame.Rect.colliderect(pumpkin_rect, green_ghost_rect)
                    and self._health_points == 0
            ):
                self._is_game_over = True

            if pygame.Rect.colliderect(pumpkin_rect, flag_rect) and self._health_points > 0:
                self._is_game_won = True

            elif pygame.Rect.colliderect(pumpkin_rect, ghost_rect) \
                    and self._ghost_alive \
                    and self._damage_taken_buffer > 1000:
                self._health_points -= 1
                self._damage_taken_buffer = 0

            elif pygame.Rect.colliderect(pumpkin_rect, green_ghost_rect) \
                    and self._green_ghost_alive \
                    and self._damage_taken_buffer > 1000:
                self._health_points -= 1
                self._damage_taken_buffer = 0

        self._printer.commit()

        if self._game_controls.should_quit():
            self._session.get().stop()

    def weapon_firing(self, delta):
        if self._game_controls.should_fire() and not self._is_weapon_out:
            self._is_weapon_out = True
            self._x_sword_position = self._x_pumpkin_position
            self._y_position_sword = self._y_position_pumpkin
        elif self._is_weapon_out:
            if self._weapon_offset >= 125:
                self._weapon_offset = 25
                self._is_weapon_out = False
            else:
                self._weapon_offset += int(5 * delta / 25)
                self._sprite_client.render_sprite(
                    Sprites.sword,
                    Position(
                        {
                            "x": self._x_sword_position + self._weapon_offset,
                            "y": int(self._y_position_sword)
                        }
                    )
                )

    def pumpkin_x_axis_movement(self, delta):
        if not self._is_game_won:
            if (self._game_controls.is_right_moving() and
                    self._x_pumpkin_position <= self._scene_right_limit-45):
                self._x_pumpkin_position += int(10 * delta / 25)

            elif self._game_controls.is_left_moving() and self._x_pumpkin_position > 5:
                self._x_pumpkin_position -= int(10 * delta / 25)

    def pumpkin_y_axis_movement(self, delta):
        if not self._is_game_won:
            if self._game_controls.should_jump() and not self._is_jumping:
                self._is_jumping = True
                self._vertical_velocity = -1.5

            self._y_position_pumpkin = \
                self._y_position_pumpkin + (self._vertical_velocity * delta / 1.5)

            self.gravity(delta)

            if self._y_position_pumpkin > 515:
                self._y_position_pumpkin = 515
                self._vertical_velocity = 0
                self._is_jumping = False

    def gravity(self, delta: int):
        self._vertical_velocity += 0.1 * delta / 15

    def heart_health(self, health_points):
        health_point_list = [
            Sprites.zero_health,
            Sprites.half_health,
            Sprites.full_health]

        self._sprite_client.render_sprite(
            health_point_list[health_points],
            self._camera.relative_position(Position({"x": 900, "y": 100}))
        )

    def walking_ghost(self, delta):
        if not self._is_game_won:
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

    def walking_green_ghost(self, delta):
        if not self._is_game_won:
            if self._ghost_moves_right:
                new_position = self._green_ghost_position + int(5 * delta / 25)
                self._green_ghost_position = new_position if new_position <= 1600 else 1600
            if not self._green_ghost_moves_right:
                new_position = self._green_ghost_position - int(5 * delta / 25)
                self._green_ghost_position = new_position if new_position >= 1200 else 1200
            if self._green_ghost_position == 1200 or self._green_ghost_position == 1600:
                self._green_ghost_moves_right = not self._green_ghost_moves_right

        self._sprite_client.render_sprite(
            Sprites.green_ghost,
            Position({"x": self._green_ghost_position, "y": 500})
        )

    def make_floor(self):
        self._sprite_client.render_sprite(
            Sprites.floor_left_corner,
            Position({"x": 0, "y": 550})
        )

        for x in range(int(2700 / 50)):
            self._sprite_client.render_sprite(
                Sprites.floor_middle,
                Position({"x": 50 + x * 50, "y": 550})
            )

        self._sprite_client.render_sprite(
            Sprites.floor_right_corner,
            Position({"x": 2750, "y": 550})
        )


class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene
