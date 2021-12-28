import logging
from abc import ABC, abstractmethod
from functools import lru_cache
from pathlib import Path
from threading import Event
from typing import Dict, Tuple

from pygame.font import Font

from seagulls.assets import AssetManager
from seagulls.engine import (
    GameControls,
    GameObject,
    GameObjectsCollection,
    IGameScene,
    Surface,
    SurfaceRenderer
)

logger = logging.getLogger(__name__)


class IShip(ABC):
    @abstractmethod
    def sprite(self) -> str:
        pass

    @abstractmethod
    def velocity(self) -> int:
        pass

    @abstractmethod
    def power(self) -> int:
        pass

    @abstractmethod
    def display_name(self) -> str:
        pass

    @abstractmethod
    def offset(self) -> int:
        pass


class OrangeShip(IShip):

    def sprite(self) -> str:
        return "space-shooter/ship-orange"

    def velocity(self) -> int:
        return 20

    def power(self) -> int:
        return 10

    def display_name(self) -> str:
        return "Orange Ship"

    def offset(self) -> int:
        return 0


class BlueShip(IShip):

    def sprite(self) -> str:
        return "space-shooter/ship-blue"

    def velocity(self) -> int:
        return 10

    def power(self) -> int:
        return 20

    def display_name(self) -> str:
        return "Blue Ship"

    def offset(self) -> int:
        return 512


class ShipButton(GameObject):

    _ship: IShip

    _asset_manager: AssetManager
    _game_controls: GameControls
    _is_highlighted: Event
    _is_clicked: Event

    _window_height = 768
    _window_width = 1024

    _button_height = 49
    _button_width = 190

    def __init__(
            self,
            ship: IShip,
            asset_manager: AssetManager):

        self._ship = ship
        self._asset_manager = asset_manager

        self._is_highlighted = Event()
        self._is_clicked = Event()

        self._font = Font(Path("assets/fonts/kenvector-future.ttf"), 14)

    def tick(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        button = self._get_background()

        text = self._font.render(self._ship.display_name(), True, (90, 90, 70))
        text_height = text.get_height()
        padding = (button.get_height() - text_height) / 2

        ship_sprite = self._asset_manager.load_sprite(self._ship.sprite()).copy()
        ship_velocity = self._font.render("Velocity: " + str(self._ship.velocity()), True,
                                          "red", "black")
        ship_power = self._font.render("Power: " + str(self._ship.power()), True,
                                       "red", "black")

        button.blit(text, (10, padding))
        surface.blit(button, (self._get_position()[0], self._get_position()[1] + 160))
        surface.blit(ship_sprite, (self._get_position()[0], self._get_position()[1]))
        surface.blit(ship_velocity, (self._get_position()[0], self._get_position()[1] + 100))
        surface.blit(ship_power, (self._get_position()[0], self._get_position()[1] + 120))

    def _get_background(self) -> Surface:
        return self._get_background_map()[self._get_state_name()]

    @lru_cache()
    def _get_background_map(self) -> Dict[str, Surface]:
        return {
            "normal": self._asset_manager.load_png("ui/blue.button00").copy(),
            "hover": self._asset_manager.load_png("ui/green.button00").copy(),
            "click": self._asset_manager.load_png("ui/green.button01").copy(),
        }

    def _get_state_name(self) -> str:
        if self._is_highlighted.is_set():
            return "click" if self._is_clicked.is_set() else "hover"

        return "normal"

    def _get_position(self) -> Tuple[int, int]:
        left = int((self._window_width / 4) - self._button_width / 2) + self._ship.offset()
        top = int((self._window_height / 4) - self._button_height / 2)
        if self._is_clicked.is_set():
            top += 5

        return left, top


class ShipCatalog:
    ships: Tuple[IShip, ...]

    def __init__(self, ships: Tuple[IShip, ...]):
        self.ships = ships


class ShipSelectionMenu(IGameScene):
    _ship_catalog: Tuple[IShip, ...]
    _surface_renderer: SurfaceRenderer
    _game_controls: GameControls
    _asset_manager: AssetManager

    _game_objects: GameObjectsCollection
    _should_quit: Event

    _red_ship_button: GameObject
    _blue_ship_button: GameObject

    def __init__(
            self,
            catalog: ShipCatalog,
            surface_renderer: SurfaceRenderer,
            asset_manager: AssetManager,
            background: GameObject,
            game_controls: GameControls):

        self._ship_catalog = catalog.ships
        self._surface_renderer = surface_renderer
        self._asset_manager = asset_manager
        self._game_controls = game_controls

        self._game_objects = GameObjectsCollection()
        self._game_objects.add(self._game_controls)
        self._game_objects.add(background)

        for ship in self._ship_catalog:
            self._game_objects.add(ShipButton(ship, self._asset_manager))

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

        self._render()

    def _render(self) -> None:
        background = Surface((1024, 600))
        self._game_objects.apply(lambda x: x.render(background))

        self._surface_renderer.render(background)
