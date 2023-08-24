from pathlib import Path

import logging

import pygame
from seagulls.assets import AssetManager
from seagulls.engine import GameClock, GameControls
from seagulls.pygame import PygamePrinter, WindowSurface
from seagulls.rendering import (
    Camera,
    Color,
    Position,
    Size,
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
    floor_single_piece = "floor-single-piece"
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
    menu_button = "menu-button"
    menu_button_text = "menu-button-text"


class RpgScene2(IGameScene):

    _session: IProvideGameSessions
    _printer: PygamePrinter
    _camera: Camera
    _asset_manager: AssetManager

    def __init__(
            self,
            session: IProvideGameSessions,
            printer: PygamePrinter,
            window: WindowSurface,
            camera: Camera,
            sprite_client: SpriteClient,
            game_controls: GameControls,
            clock: GameClock,
            asset_manager: AssetManager):
        self._session = session
        self._printer = printer
        self._window = window
        self._camera = camera
        self._sprite_client = sprite_client
        self._game_controls = game_controls
        self._clock = clock
        self._asset_manager = asset_manager
        self._scene_right_limit = 3200
        self._x_pumpkin_position = 10
        self._y_position_pumpkin = 515.0
        self._x_position_flag_banner = self._scene_right_limit - 200
        self._y_position_flag_banner = 450
        self._x_position_flag_pole = self._scene_right_limit - 200
        self._y_position_flag_pole = 500
        self._vertical_velocity = 0.0
        self._ghost_position = 400
        self._green_ghost_position = 1200
        self._hole_position = 2800
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
        self._lava = pygame.Rect((0, 750), (self._scene_right_limit, 50))

    def tick(self) -> None:
        self._printer.clear()
        self._game_controls.tick()

        self._clock.tick()

        fps = self._clock.get_fps()

        self.render_fps(fps)

        delta = self._clock.get_time()
        self._damage_taken_buffer += delta

        self.make_floor()
        self.heart_health(self._health_points)

        if self._is_game_won:
            self._printer.print_text(
                "You win!", Path("seagulls_assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 100,
                Color({"r": 250, "g": 140, "b": 0}), Size({"height": 200, "width": 150}),
                self._camera.relative_position(Position({"x": 300, "y": 0})))

            self._sprite_client.render_sprite(
                Sprites.menu_button,
                self._camera.relative_position(
                    Position({"x": 350, "y": 350}))
            )
            self._printer.print_text(
                "Main Menu", Path("seagulls_assets/fonts/ubuntu-mono-v10-latin-regular.ttf"), 100,
                Color({"r": 250, "g": 69, "b": 0}), Size({"height": 80, "width": 60}),
                self._camera.relative_position(Position({"x": 450, "y": 340})))

        if self._ghost_alive:
            self.walking_ghost(delta)

        if self._green_ghost_alive:
            self.walking_green_ghost(delta)

        if self._is_game_over:
            self._sprite_client.render_sprite(
                Sprites.dead_pumpkin,
                Position({"x": self._x_pumpkin_position, "y": int(self._y_position_pumpkin)})
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
                    (pygame.Rect.colliderect(pumpkin_rect, ghost_rect)
                        or pygame.Rect.colliderect(pumpkin_rect, green_ghost_rect))
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

    def render_fps(self, fps: float) -> None:
        self._printer.print_text(
            str(int(fps)),
            self._asset_manager.get_path("fonts/ubuntu-mono-v10-latin-regular.ttf"),
            32,
            Color({"r": 16, "g": 16, "b": 16}),
            Size({"height": 32, "width": 64}),
            self._camera.relative_position(Position({"x": 900, "y": 200})))

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

            pumpkin_rect = pygame.Rect((self._x_pumpkin_position, self._y_position_pumpkin),
                                       (35, 35))

            hole_rect = pygame.Rect((self._hole_position, 550), (
                self._scene_right_limit - 125 - self._hole_position, 50))

            if (self._y_position_pumpkin > 515
                    and not pygame.Rect.colliderect(pumpkin_rect, hole_rect)):
                self._y_position_pumpkin = 515
                self._vertical_velocity = 0
                self._is_jumping = False

            if pygame.Rect.colliderect(self._lava, pumpkin_rect):
                self._is_game_over = True

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
            Position({"x": 2750, "y": 550}))

        self._sprite_client.render_sprite(
            Sprites.floor_single_piece,
            Position({"x": self._scene_right_limit - 225, "y": 550}))

    def make_button(self):
        self._sprite_client.render_sprite(
            Sprites.menu_button,
            Position({"x": 100, "y": 100})
        )
#
# button.blit(text, (10, padding))
#         surface.blit(button, (self._get_position()[0], self._get_position()[1] + 160))
#         surface.blit(ship_sprite, (self._get_position()[0], self._get_position()[1]))
#         surface.blit(ship_velocity, (self._get_position()[0], self._get_position()[1] + 100))
#         surface.blit(ship_power, (self._get_position()[0], self._get_position()[1] + 120))
#
#     def _detect_state(self) -> None:
#         _button_width = self._get_button_width()
#         _button_height = self._get_button_height()
#         rect = Rect(
#             (self._get_position()[0], self._get_position()[1] + 160),
#             (_button_width,
#              _button_height))
#
#         if rect.collidepoint(pygame.mouse.get_pos()):
#             self._is_highlighted.set()
#             click = self._game_controls.is_click_initialized()
#             if click:
#                 logger.debug("CLICKY")
#                 self._is_clicked.set()
#             if not self._game_controls.is_mouse_down():
#                 if self._is_clicked.is_set():
#                     logger.debug("SWITCH")
#                     # TODO fix typing issue below
#                     self._scene.reset()  # type: ignore
#                     self._active_scene_manager.set_active_scene(self._scene)
#                     self._active_ship_manager.set_active_ship(self._ship)
#                 self._is_clicked.clear()
#         else:
#             self._is_highlighted.clear()
#             self._is_clicked.clear()

class SceneProvider(IProvideGameScenes):

    _scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._scene = scene

    def get(self) -> IGameScene:
        return self._scene
