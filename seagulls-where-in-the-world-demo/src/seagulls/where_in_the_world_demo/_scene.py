from datetime import datetime
from functools import lru_cache

from math import ceil, hypot
from typing import Tuple, List, Optional, Dict, Any

import pygame.font
import pygame.mouse
import pygame.transform
import yaml
from pygame import Surface, Rect

from seagulls.assets import AssetManager
from ._main import GameInputClient
from ._session_window_client import GameSessionWindowClient

from ._animals import animal_names
from ._countries_client import CountriesClient
from ._dishes_client import IDishesClient
from ._position import Position
from ._state import GameState
from ._size import Size
from ._ui import PixelUi, BoxSurfaces
from ._shots_client import ShotsClient, Shot


class MainScene:
    _game_input_client: GameInputClient
    _session_window_client: GameSessionWindowClient
    _asset_manager: AssetManager
    _shots_client: ShotsClient
    _countries_client: CountriesClient
    _dishes_client: IDishesClient
    _players: Tuple[str, ...]
    _player_scores: List[int]

    _fired_shots_list: List[Tuple[int, int]]
    _player_shot: Optional[Tuple[int, int]]
    _player_shot_button_down: bool

    _play_button_position: Tuple[int, int]
    _play_button_down: bool

    _game_state: GameState
    _game_state_toggled_at: datetime

    _current_player: int
    _current_level: int

    _scene_created_at: datetime

    def __init__(
            self,
            game_input_client: GameInputClient,
            session_window_client: GameSessionWindowClient,
            asset_manager: AssetManager,
            shots_client: ShotsClient,
            countries_client: CountriesClient,
            dishes_client: IDishesClient,
            players: Tuple[str, ...]) -> None:
        self._game_input_client = game_input_client
        self._session_window_client = session_window_client
        self._asset_manager = asset_manager
        self._shots_client = shots_client
        self._countries_client = countries_client
        self._dishes_client = dishes_client
        self._players = players
        self._player_scores = [0 for _ in players]

        self._fired_shots_list = []
        self._player_shot = None
        self._player_shot_button_down = False
        self._play_button_position = (915, 790)
        self._play_button_down = False

        self._set_state(GameState.MENU)

        self._current_player = 0
        self._current_level = 0

        self._scene_created_at = datetime.now()

    def update(self) -> None:
        if self._is_state(GameState.MENU):
            self._update_menu()
        elif self._is_state(GameState.LEVEL):
            self._update_level()
        elif self._is_state(GameState.LEVEL_END):
            self._update_level_end()
        elif self._is_state(GameState.GAME_END):
            self._update_game_end()

    def _update_menu(self) -> None:
        if self._game_input_client.was_mouse_button_pressed():
            play_button_rect = Rect(self._play_button_position, (110, 45))
            if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                self._play_button_down = True

        if self._game_input_client.was_mouse_button_released():
            play_button_rect = Rect(self._play_button_position, (110, 45))
            if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                self._set_state(GameState.LEVEL)

            self._play_button_down = False

    def _update_level(self) -> None:
        if self._player_shot:
            if self._game_input_client.was_mouse_button_pressed():
                button_rect = Rect(
                    (self._player_shot[0] + 30, self._player_shot[1] - 50), (110, 45))
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    self._player_shot_button_down = True

        if self._game_input_client.was_mouse_button_released():
            if self._player_shot_button_down:
                button_rect = Rect(
                    (self._player_shot[0] + 30, self._player_shot[1] - 50), (110, 45))
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    # User has accepted the shot
                    self._fired_shots_list.append(self._player_shot)
                    self._shots_client.add(Shot(
                        player=self._current_player,
                        level=self._current_level,
                        position=Position(self._player_shot[0], self._player_shot[1]),
                    ))

                    # Update the player score
                    shot = self._shots_client.get_player_level_shot(
                        self._current_player,
                        self._current_level,
                    )
                    dish = self._dishes_client.get_level(self._current_level)
                    country = self._countries_client.get_country(dish.country)
                    answer = country.position
                    attempt = shot.position
                    distance = int(abs(hypot(answer.x - attempt.x, answer.y - attempt.y)) / 10)
                    self._player_scores[self._current_player] += distance

                    self._player_shot = None
                    self._current_player += 1
                    if self._current_player == len(self._players):
                        self._current_player = 0
                        self._set_state(GameState.LEVEL_END)
            else:
                self._player_shot = pygame.mouse.get_pos()
            self._player_shot_button_down = False

    def _update_level_end(self) -> None:
        if self._game_input_client.was_mouse_button_pressed():
            play_button_rect = Rect(self._play_button_position, (110, 45))
            if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                self._play_button_down = True

        if self._game_input_client.was_mouse_button_released():
            play_button_rect = Rect(self._play_button_position, (110, 45))
            if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self._dishes_client.is_final_level(self._current_level):
                    self._set_state(GameState.GAME_END)
                else:
                    self._current_level += 1
                    self._set_state(GameState.LEVEL)

            self._play_button_down = False

    def _update_game_end(self) -> None:
        pass

    def render(self) -> None:
        window = self._window()

        window.fill((240, 240, 240))
        window.blit(self._map(), (0, 0))
        window.blit(self._ocean_creatures(), (0, 0))
        window.blit(self._countries(), (0, 0))
        window.blit(self._fired_shots(), (0, 0))
        window.blit(self._menu(), (0, 0))
        window.blit(self._character(), (0, 0))
        window.blit(self._dish_clue(), (0, 0))
        window.blit(self._dish_image(), (0, 0))
        window.blit(self._cursor(), pygame.mouse.get_pos())

    def _menu(self) -> Surface:
        ui = self._get_pixel_ui()
        surface = self._make_layer()
        toggle_delta = (datetime.now() - self._game_state_toggled_at)
        toggle_delta_ms = toggle_delta.microseconds
        toggle_delta_s = toggle_delta.total_seconds()
        if self._is_state(GameState.LEVEL) and toggle_delta_s >= 1:
            return surface

        positions = [
            (760, 230),
            (970, 230),
            (760, 340),
            (970, 340),
            (760, 450),
            (970, 450),
            (760, 560),
            (970, 560),
            (760, 670),
            (970, 670),
        ]

        menu_background = self._make_box(
            grid=BoxSurfaces(
                top_left=ui.panel_top_left_light_brown,
                top=ui.panel_top_light_brown,
                top_right=ui.panel_top_right_light_brown,
                left=ui.panel_left_light_brown,
                center=ui.panel_center_light_brown,
                right=ui.panel_right_light_brown,
                bottom_left=ui.panel_bottom_left_light_brown,
                bottom=ui.panel_bottom_light_brown,
                bottom_right=ui.panel_bottom_right_light_brown,
            ),
            size=Size(451, 650)
        )

        dialog = self._make_box(
            grid=BoxSurfaces(
                top_left=ui.panel_top_left_light_grey,
                top=ui.panel_top_light_grey,
                top_right=ui.panel_top_right_light_grey,
                left=ui.panel_left_light_grey,
                center=ui.panel_center_light_grey,
                right=ui.panel_right_light_grey,
                bottom_left=ui.panel_bottom_left_light_grey,
                bottom=ui.panel_bottom_light_grey,
                bottom_right=ui.panel_bottom_right_light_grey,
            ),
            size=Size(411, 210)
        )

        def render_multi_line(lines: List[str]) -> None:
            for y, line in enumerate(lines):
                dialog.blit(
                    text_font.render(line, True, (80, 80, 80)), (10, 35 + (y * 20)))

        title_font = pygame.font.SysFont("Ubuntu Mono", 24)
        text_font = pygame.font.SysFont("Ubuntu Mono", 16)
        if self._is_state(GameState.MENU):
            dialog.blit(title_font.render("Welcome!", True, (80, 80, 80)), (10, 10))
            render_multi_line([
                "Thanks for celebrating Laura's birthday with us!",
                "Listen up while I explain the rules of the game!",
                "",
                "",
                "",
                "",
                "",
                "  — Cartographer Lolo",
            ])
        elif self._is_state(GameState.LEVEL_END):
            dish = self._dishes_client.get_level(self._current_level)
            dialog.blit(title_font.render(
                f"{dish.name} from {dish.country}!", True, (80, 80, 80)), (10, 10))
            render_multi_line(dish.description)

        elif self._is_state(GameState.GAME_END):
            dialog.blit(title_font.render(f"Bye!", True, (80, 80, 80)), (10, 10))
            render_multi_line([
                "Thanks for joining us for this adventure!",
                "I ran out of time so I don't know who the",
                "winner is but y'all can figure it out!",
                "  — Cartographer Lolo",
            ])

        surface.blit(menu_background, (740, 210))
        surface.blit(dialog, (758, 560))
        surface.blit(self._get_dialog_character(), (0, 0))

        for x, player in enumerate(self._players):
            surface.blit(self._player_card(animal_names[x], player), positions[x])

        if not self._is_state(GameState.GAME_END):
            surface.blit(self._menu_buttons(), (0, 0))

        if self._is_state(GameState.LEVEL) and toggle_delta_ms > 0:
            new_surface = self._make_layer()
            new_surface.blit(surface, (0, toggle_delta_ms * toggle_delta_ms / 400000000))
            return new_surface.subsurface((0, 0), (1920, 1080))

        return surface

    def _get_dialog_character(self) -> Surface:
        ui = self._get_pixel_ui()
        surface = self._make_layer()

        dialog_character = self._make_box(
            grid=BoxSurfaces(
                top_left=ui.panel_top_left_light_brown,
                top=ui.panel_top_light_brown,
                top_right=ui.panel_top_right_light_brown,
                left=ui.panel_left_light_brown,
                center=ui.panel_center_light_brown,
                right=ui.panel_right_light_brown,
                bottom_left=ui.panel_bottom_left_light_brown,
                bottom=ui.panel_bottom_light_brown,
                bottom_right=ui.panel_bottom_right_light_brown,
            ),
            size=Size(170, 170)
        )
        if self._is_state(GameState.MENU):
            dialog_character.blit(self._get_cartographer_lolo(), (10, 10))
            surface.blit(dialog_character, (558, 560))
        elif self._is_state(GameState.LEVEL) and self._current_level == 0:
            dialog_character.blit(self._get_cartographer_lolo(), (10, 10))
            surface.blit(dialog_character, (558, 560))
        elif self._is_state(GameState.GAME_END):
            dialog_character.blit(self._get_cartographer_lolo(), (10, 10))
            surface.blit(dialog_character, (558, 560))
        else:
            dialog_character.blit(self._get_companion_fitz(), (10, 10))
            surface.blit(dialog_character, (1200, 560))

        return surface

    def _character(self) -> Surface:
        surface = self._make_layer()
        if not self._is_state(GameState.LEVEL):
            return surface

        card = self._player_card(
            animal_names[self._current_player], self._players[self._current_player])

        surface.blit(card, (873, 970))

        return surface

    def _dish_clue(self) -> Surface:
        surface = self._make_layer()
        if not self._is_state(GameState.LEVEL):
            return surface

        ui = self._get_pixel_ui()

        dialog = self._make_box(
            grid=BoxSurfaces(
                top_left=ui.panel_top_left_light_grey,
                top=ui.panel_top_light_grey,
                top_right=ui.panel_top_right_light_grey,
                left=ui.panel_left_light_grey,
                center=ui.panel_center_light_grey,
                right=ui.panel_right_light_grey,
                bottom_left=ui.panel_bottom_left_light_grey,
                bottom=ui.panel_bottom_light_grey,
                bottom_right=ui.panel_bottom_right_light_grey,
            ),
            size=Size(411, 200)
        )

        def render_multi_line(lines: List[str]) -> None:
            for y, line in enumerate(lines):
                dialog.blit(
                    text_font.render(line, True, (80, 80, 80)), (10, 35 + (y * 20)))

        dish = self._dishes_client.get_level(self._current_level)

        title_font = pygame.font.SysFont("Ubuntu Mono", 24)
        text_font = pygame.font.SysFont("Ubuntu Mono", 16)

        dialog.blit(title_font.render("Clue!", True, (80, 80, 80)), (10, 10))
        render_multi_line(dish.description)

        surface.blit(dialog, (10, 870))

        return surface

    def _dish_image(self) -> Surface:
        surface = self._make_layer()
        if not self._is_state(GameState.LEVEL_END):
            return surface

        ui = self._get_pixel_ui()
        dialog_dish = self._make_box(
            grid=BoxSurfaces(
                top_left=ui.panel_top_left_light_brown,
                top=ui.panel_top_light_brown,
                top_right=ui.panel_top_right_light_brown,
                left=ui.panel_left_light_brown,
                center=ui.panel_center_light_brown,
                right=ui.panel_right_light_brown,
                bottom_left=ui.panel_bottom_left_light_brown,
                bottom=ui.panel_bottom_light_brown,
                bottom_right=ui.panel_bottom_right_light_brown,
            ),
            size=Size(170, 170)
        )

        dialog_dish.blit(self._dishes_client.get_dish_image(self._current_level), (10, 10))
        surface.blit(dialog_dish, (558, 560))

        return surface

    def _player_card(self, animal: str, name: str) -> Surface:
        ui = self._get_pixel_ui()
        card_width = 200
        card_height = 100

        card = self._make_box(
            grid=BoxSurfaces(
                top_left=ui.panel_top_left_dark_brown,
                top=ui.panel_top_dark_brown,
                top_right=ui.panel_top_right_dark_brown,
                left=ui.panel_left_dark_brown,
                center=ui.panel_center_dark_brown,
                right=ui.panel_right_dark_brown,
                bottom_left=ui.panel_bottom_left_dark_brown,
                bottom=ui.panel_bottom_dark_brown,
                bottom_right=ui.panel_bottom_right_dark_brown,
            ),
            size=Size(card_width, card_height)
        )

        details_height = 75
        details_width = 85

        details = self._make_box(
            grid=BoxSurfaces(
                top_left=ui.panel_top_left_light_brown,
                top=ui.panel_top_light_brown,
                top_right=ui.panel_top_right_light_brown,
                left=ui.panel_left_light_brown,
                center=ui.panel_center_light_brown,
                right=ui.panel_right_light_brown,
                bottom_left=ui.panel_bottom_left_light_brown,
                bottom=ui.panel_bottom_light_brown,
                bottom_right=ui.panel_bottom_right_light_brown,
            ),
            size=Size(details_width, details_height)
        )

        if self._is_state(GameState.MENU):
            score = f" -"
        elif self._is_state(GameState.LEVEL):
            score = f"{self._player_scores[self._get_player_id(name)]:04}"
        elif self._is_state(GameState.LEVEL_END):
            shot = self._shots_client.get_player_level_shot(
                self._get_player_id(name), self._current_level)
            dish = self._dishes_client.get_level(self._current_level)
            country = self._countries_client.get_country(dish.country)
            answer = country.position
            attempt = shot.position
            distance = int(abs(hypot(answer.x - attempt.x, answer.y - attempt.y)) / 10)
            score = f"+{distance:03}"
        else:
            score = f"{self._player_scores[self._get_player_id(name)]:04}"

        title_font = pygame.font.SysFont("Ubuntu Mono", 16)
        score_font = pygame.font.SysFont("Ubuntu Mono", 32)
        details.blit(title_font.render(name, True, (80, 80, 80)), (10, 10))
        details.blit(score_font.render(score, True, (80, 80, 80)), (10, 30))

        card.blit(details, (100, 12))

        animal = self._asset_manager.load_png(
            f"kenney.animal-pack/png.square.no-details.outline/{animal}")
        card.blit(pygame.transform.scale(animal, (75, 75)), (12, 12))
        return card

    def _menu_buttons(self) -> Surface:
        surface = self._make_layer()

        font = pygame.font.SysFont("Ubuntu Mono", 20)

        if self._play_button_down:
            full = self._get_ui("button-long-blue-pressed")
            button_right = full.subsurface((full.get_width() - 10, 0), (10, full.get_height()))
            button = full.subsurface((0, 0), (90, full.get_height()))
            position = (self._play_button_position[0], self._play_button_position[1] + 2)
        else:
            full = self._get_ui("button-long-blue")
            button_right = full.subsurface((full.get_width() - 10, 0), (10, full.get_height()))
            button = full.subsurface((0, 0), (90, full.get_height()))
            position = self._play_button_position

        surface.blit(button, position)
        surface.blit(button_right, (position[0] + 90, position[1]))
        surface.blit(
            self._get_ui("icon-check-blue"),
            (position[0] + 15, position[1] + 15),
        )
        if self._is_state(GameState.MENU):
            surface.blit(
                font.render("Play!", True, (160, 160, 160)),
                (position[0] + 35, position[1] + 12),
            )
        elif self._is_state(GameState.LEVEL_END):
            surface.blit(
                font.render("Next!", True, (160, 160, 160)),
                (position[0] + 35, position[1] + 12),
            )

        return surface

    def _fired_shots(self) -> Surface:
        surface = self._make_layer()
        spritesheet = self._asset_manager.load_png("kenney.pixel-ui-pack/spritesheet")

        bullet_orange = Surface((16, 16), pygame.SRCALPHA, 32).convert_alpha()
        bullet_orange.blit(spritesheet, (-1 * (18 * 21), -1 * (18 * 6)))
        bullet_yellow = Surface((16, 16), pygame.SRCALPHA, 32).convert_alpha()
        bullet_yellow.blit(spritesheet, (-1 * (18 * 9), -1 * (18 * 6)))
        bullet_green = Surface((16, 16), pygame.SRCALPHA, 32).convert_alpha()
        bullet_green.blit(spritesheet, (-1 * (18 * 15), -1 * (18 * 6)))
        bullet_white = Surface((16, 16), pygame.SRCALPHA, 32).convert_alpha()
        bullet_white.blit(spritesheet, (-1 * (18 * 3), -1 * (18 * 6)))
        bullet_grey = Surface((16, 16), pygame.SRCALPHA, 32).convert_alpha()
        bullet_grey.blit(spritesheet, (-1 * (18 * 3), -1 * (18 * 23)))

        for shot in self._fired_shots_list:
            position = (shot[0] - 8, shot[1] - 7)
            surface.blit(bullet_green, position)

        if self._player_shot:
            font = pygame.font.SysFont("Ubuntu Mono", 20)

            if self._player_shot_button_down:
                full = self._get_ui("button-long-blue-pressed")
                button_right = full.subsurface((180, 0), (10, 45))
                button = full.subsurface((0, 0), (100, 45))
                button_position = (self._player_shot[0] + 30, self._player_shot[1] - 47)
            else:
                full = self._get_ui("button-long-blue")
                button_right = full.subsurface((180, 0), (10, 49))
                button = full.subsurface((0, 0), (100, 49))
                button_position = (self._player_shot[0] + 30, self._player_shot[1] - 50)

            bullet_position = (self._player_shot[0] - 8, self._player_shot[1] - 7)
            surface.blit(bullet_orange, bullet_position)
            surface.blit(button, button_position)
            surface.blit(button_right, (button_position[0] + 100, button_position[1]))
            surface.blit(
                self._get_ui("icon-check-blue"),
                (button_position[0] + 15, button_position[1] + 15),
            )
            surface.blit(
                font.render("Accept", True, (160, 160, 160)),
                (button_position[0] + 35, button_position[1] + 12),
            )

        return surface

    @lru_cache()
    def _get_pixel_ui(self) -> PixelUi:
        spritesheet = self._asset_manager.load_png("kenney.pixel-ui-pack/spritesheet")

        def _make(x: int, y: int) -> Surface:
            surface = Surface((16, 16), pygame.SRCALPHA, 32)
            surface.blit(spritesheet, (-1 * (18 * x), -1 * (18 * y)))
            return surface

        return PixelUi(
            bullet_orange=_make(21, 6),
            bullet_yellow=_make(9, 6),
            bullet_green=_make(15, 6),
            bullet_white=_make(3, 6),
            bullet_grey=_make(3, 23),

            panel_top_left_dark_brown=pygame.transform.scale2x(_make(6, 13)),
            panel_top_dark_brown=pygame.transform.scale2x(_make(7, 13)),
            panel_top_right_dark_brown=pygame.transform.scale2x(_make(8, 13)),
            panel_left_dark_brown=pygame.transform.scale2x(_make(6, 14)),
            panel_center_dark_brown=pygame.transform.scale2x(_make(7, 14)),
            panel_right_dark_brown=pygame.transform.scale2x(_make(8, 14)),
            panel_bottom_left_dark_brown=pygame.transform.scale2x(_make(6, 15)),
            panel_bottom_dark_brown=pygame.transform.scale2x(_make(7, 15)),
            panel_bottom_right_dark_brown=pygame.transform.scale2x(_make(8, 15)),

            panel_top_left_light_brown=pygame.transform.scale2x(_make(9, 13)),
            panel_top_light_brown=pygame.transform.scale2x(_make(10, 13)),
            panel_top_right_light_brown=pygame.transform.scale2x(_make(11, 13)),
            panel_left_light_brown=pygame.transform.scale2x(_make(9, 14)),
            panel_center_light_brown=pygame.transform.scale2x(_make(10, 14)),
            panel_right_light_brown=pygame.transform.scale2x(_make(11, 14)),
            panel_bottom_left_light_brown=pygame.transform.scale2x(_make(9, 15)),
            panel_bottom_light_brown=pygame.transform.scale2x(_make(10, 15)),
            panel_bottom_right_light_brown=pygame.transform.scale2x(_make(11, 15)),

            panel_top_left_light_grey=pygame.transform.scale2x(_make(0, 13)),
            panel_top_light_grey=pygame.transform.scale2x(_make(1, 13)),
            panel_top_right_light_grey=pygame.transform.scale2x(_make(2, 13)),
            panel_left_light_grey=pygame.transform.scale2x(_make(0, 14)),
            panel_center_light_grey=pygame.transform.scale2x(_make(1, 14)),
            panel_right_light_grey=pygame.transform.scale2x(_make(2, 14)),
            panel_bottom_left_light_grey=pygame.transform.scale2x(_make(0, 15)),
            panel_bottom_light_grey=pygame.transform.scale2x(_make(1, 15)),
            panel_bottom_right_light_grey=pygame.transform.scale2x(_make(2, 15)),
        )

    @lru_cache()
    def _get_ui(self, name: str) -> Surface:
        spritesheet = self._asset_manager.load_png("kenney.rpg-ui-pack/spritesheet")
        mapping = self._ui_mapping()

        config = mapping[name]
        x = config["x"]
        y = config["y"]
        width = config["width"]
        height = config["height"]

        ui = Surface((width, height), pygame.SRCALPHA, 32)
        ui.blit(spritesheet, (-1 * x, -1 * y))

        return ui

    @lru_cache()
    def _ui_mapping(self) -> Dict[str, Any]:
        spritesheet_yaml = self._asset_manager.get_path("kenney.rpg-ui-pack/spritesheet.yaml")
        return yaml.safe_load(spritesheet_yaml.read_text())

    @lru_cache()
    def _map(self) -> Surface:
        surface = self._asset_manager.load_png("maps/003")

        return pygame.transform.scale(surface, (1920, 1080))

    def _ocean_creatures(self) -> Surface:
        surface = self._make_layer()

        frequency_ms = 10000
        duration_ms = 1500

        current_time_ms = self._scene_age_ms()

        remainder = current_time_ms % frequency_ms
        iteration = int(current_time_ms / frequency_ms)

        versions = [
            {
                "start_rotation": 20,
                "end_rotation": 90,
                "start_x": 800,
                "start_y": 800,
                "end_x": 100,
                "end_y": 800,
            },
            {
                "start_rotation": -60,
                "end_rotation": -80,
                "start_x": 1500,
                "start_y": 800,
                "end_x": 1900,
                "end_y": 400,
            },
            {
                "start_rotation": -90,
                "end_rotation": -180,
                "start_x": 80,
                "start_y": 300,
                "end_x": 1000,
                "end_y": 400,
            },
        ]

        if remainder < duration_ms:
            version_index = iteration % (len(versions))
            version = versions[version_index]
            diff_x = version["end_x"] - version["start_x"]
            diff_y = version["end_y"] - version["start_y"]
            diff_rotation = version["end_rotation"] - version["start_rotation"]

            # ms completed in our animation
            progress_ms = remainder
            # % completed in our animation
            progress = progress_ms / duration_ms

            current_position = (
                version["start_x"] + diff_x * progress,
                version["start_y"] + diff_y * progress,
            )

            card = Surface((100, 100), pygame.SRCALPHA, 32)
            card.blit(self._get_companion_momo(), (0, 100 - progress * 300))

            momo = pygame.transform.rotate(
                card, version["start_rotation"] + diff_rotation * progress)

            surface.blit(momo, current_position)

        return surface

    def _make_box(self, grid: BoxSurfaces, size: Size) -> Surface:
        col_width = grid.top.get_width()
        num_centers = ceil((size.width - col_width) / col_width)

        surface = Surface((size.width, size.height), pygame.SRCALPHA, 32)

        for x in range(num_centers):
            surface.blit(
                self._make_column(
                    grid.top,
                    grid.center,
                    grid.bottom,
                    size.height),
                (col_width + col_width * x, 0),
            )

        surface.blit(
            self._make_column(
                grid.top_left,
                grid.left,
                grid.bottom_left,
                size.height),
            (0, 0),
        )
        surface.blit(
            self._make_column(
                grid.top_right,
                grid.right,
                grid.bottom_right,
                size.height),
            (size.width - col_width, 0),
        )

        return surface

    def _make_column(self, top: Surface, center: Surface, bottom: Surface, height: int) -> Surface:
        width = top.get_width()
        t_height = top.get_height()
        c_height = center.get_height()
        b_height = bottom.get_height()

        column = Surface((width + 10, height + 10), pygame.SRCALPHA, 32)
        num_centers = ceil((height - t_height - b_height) / c_height)

        column.blit(top, (0, 0))
        for y in range(num_centers):
            column.blit(center, (0, t_height + c_height * y))
        column.blit(bottom, (0, height - b_height))

        return column

    @lru_cache()
    def _countries(self) -> Surface:
        spritesheet = self._asset_manager.load_png("kenney.pixel-ui-pack/spritesheet")
        font = pygame.font.SysFont("Ubuntu Mono, Bold", 30)

        map_surface = self._make_layer()

        bullet = Surface((16, 16), pygame.SRCALPHA, 32).convert_alpha()
        bullet.blit(spritesheet, (-1 * (18 * 29), -1 * (18 * 5)))

        def _annotate_country(name: str, position: Position) -> None:
            map_surface.blit(bullet, position)
            map_surface.blit(
                font.render(name, True, (10, 10, 10)), (position.x + 20, position.y - 12))
            map_surface.blit(
                font.render(name, True, (200, 200, 200)), (position.x + 21, position.y - 13))

        for country in self._countries_client.get_countries():
            _annotate_country(country.name, country.position)

        return map_surface

    @lru_cache()
    def _cursor(self) -> Surface:
        spritesheet = self._asset_manager.load_png("kenney.pixel-ui-pack/spritesheet")

        surface = Surface((16, 16), pygame.SRCALPHA, 32).convert_alpha()
        surface.blit(spritesheet, (-1 * (18 * 7), -1 * (18 * 32)))

        return pygame.transform.scale2x(surface)

    def _is_state(self, state: GameState) -> bool:
        return self._game_state == state

    def _state_age_s(self) -> int:
        return int(self._state_age_ms() / 1000)

    def _state_age_ms(self) -> int:
        now = datetime.now()
        return int((now - self._game_state_toggled_at).microseconds / 1000)

    def _scene_age_s(self) -> int:
        return int(self._scene_age_ms() / 1000)

    def _scene_age_ms(self) -> int:
        now = datetime.now().timestamp()
        return int((now - self._scene_created_at.timestamp()) * 1000)

    def _set_state(self, state: GameState) -> None:
        self._game_state = state
        self._game_state_toggled_at = datetime.now()

    def _make_layer(self) -> Surface:
        return Surface((1920, 1080), pygame.SRCALPHA, 32)

    @lru_cache()
    def _get_cartographer_lolo(self) -> Surface:
        surface = self._asset_manager.load_jpg("characters/cartogra-lolo")
        return pygame.transform.scale(surface, (150, 150))

    @lru_cache()
    def _get_companion_fitz(self) -> Surface:
        surface = self._asset_manager.load_png("characters/fitz")

        return pygame.transform.scale(surface, (150, 150))

    @lru_cache()
    def _get_companion_momo(self) -> Surface:
        surface = self._asset_manager.load_png("characters/momo")

        return pygame.transform.scale(surface, (100, 100))

    def _get_player_id(self, name: str) -> int:
        for x, player in enumerate(self._players):
            if player == name:
                return x

        raise RuntimeError(f"Player not found: {name}")

    def _window(self) -> Surface:
        return self._session_window_client.get_surface()
