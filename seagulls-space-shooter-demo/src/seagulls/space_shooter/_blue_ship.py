import logging

from ._ship_interfaces import IShip
from .fit_to_screen import FitToScreen

logger = logging.getLogger(__name__)


class BlueShip(IShip):
    _fit_to_screen: FitToScreen

    def __init__(self, fit_to_screen: FitToScreen):
        self._fit_to_screen = fit_to_screen

    def sprite(self) -> str:
        return "space-shooter/ship-blue"

    def velocity(self) -> int:
        return 3

    def power(self) -> int:
        return 20

    def display_name(self) -> str:
        return "Blue Ship"

    def offset(self) -> int:
        return int(self._fit_to_screen.get_actual_surface_width() / 3)

