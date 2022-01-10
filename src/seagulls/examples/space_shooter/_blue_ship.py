import logging

from ._ship_interfaces import IShip

logger = logging.getLogger(__name__)


class BlueShip(IShip):

    def sprite(self) -> str:
        return "space-shooter/ship-blue"

    def velocity(self) -> int:
        return 3

    def power(self) -> int:
        return 20

    def display_name(self) -> str:
        return "Blue Ship"

    def offset(self) -> int:
        return 512
