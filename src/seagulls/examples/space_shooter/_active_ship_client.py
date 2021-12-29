from abc import ABC, abstractmethod
from typing import Callable

from seagulls.examples.space_shooter._selectable_ship_menu import IShip


class IProvideActiveShip(ABC):

    @abstractmethod
    def get_active_ship(self) -> IShip:
        pass


class ISetActiveShip(ABC):

    @abstractmethod
    def set_active_ship(self, ship: IShip) -> None:
        pass


class ActiveShipClient(IProvideActiveShip, ISetActiveShip):

    _active_ship: IShip

    def __init__(self, ship: IShip):
        self._active_ship = ship

    def get_active_ship(self) -> IShip:
        return self._active_ship

    def set_active_ship(self, ship: IShip) -> None:
        self._active_ship = ship
