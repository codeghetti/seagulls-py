from ._ship_interfaces import IShip


class EmptyShip(IShip):

    def sprite(self) -> str:
        raise RuntimeError("I have no sprite, I'm empty.")

    def velocity(self) -> int:
        raise RuntimeError("I have no velocity, I'm empty.")

    def power(self) -> int:
        raise RuntimeError("I have no power, I'm empty.")

    def display_name(self) -> str:
        raise RuntimeError("I have no display name, I'm empty.")

    def offset(self) -> int:
        raise RuntimeError("I have no offset, I'm empty.")
