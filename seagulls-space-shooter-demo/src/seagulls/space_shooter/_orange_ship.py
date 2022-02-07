import logging

from ._fit_to_screen import FitToScreen
from ._ship_interfaces import IShip

logger = logging.getLogger(__name__)


class OrangeShip(IShip):

    _fit_to_screen: FitToScreen

    def __init__(self, fit_to_screen: FitToScreen):
        self._fit_to_screen = fit_to_screen

    def sprite(self) -> str:
        return "space-shooter/ship-orange"

    def velocity(self) -> int:
        return 15

    def power(self) -> int:
        return 10

    def display_name(self) -> str:
        return "Orange Ship"

    def offset(self) -> int:
        return 0
