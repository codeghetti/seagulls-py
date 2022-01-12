import logging

from ._ship_interfaces import IShip

logger = logging.getLogger(__name__)


class OrangeShip(IShip):

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
