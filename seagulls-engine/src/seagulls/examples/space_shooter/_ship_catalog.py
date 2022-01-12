import logging
from typing import Tuple

from ._ship_interfaces import IShip

logger = logging.getLogger(__name__)


class ShipCatalog:
    ships: Tuple[IShip, ...]

    def __init__(self, ships: Tuple[IShip, ...]):
        self.ships = ships
