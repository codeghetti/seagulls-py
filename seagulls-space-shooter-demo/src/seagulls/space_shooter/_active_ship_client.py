from ._ship_interfaces import IProvideActiveShip, ISetActiveShip, IShip


class ActiveShipClient(IProvideActiveShip, ISetActiveShip):

    _active_ship: IShip

    def __init__(self, ship: IShip):
        self._active_ship = ship

    def get_active_ship(self) -> IShip:
        return self._active_ship

    def set_active_ship(self, ship: IShip) -> None:
        self._active_ship = ship
