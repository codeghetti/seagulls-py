import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class IShip(ABC):
    @abstractmethod
    def sprite(self) -> str:
        """This method returns the path to the sprite"""

    @abstractmethod
    def velocity(self) -> int:
        """This method returns the velocity of the ship"""

    @abstractmethod
    def power(self) -> int:
        """This method returns the power of the ship"""

    @abstractmethod
    def display_name(self) -> str:
        """This method returns the display name for the ship"""

    @abstractmethod
    def offset(self) -> int:
        """This method provides the offset from the other ships during the ship selection"""


class IProvideActiveShip(ABC):

    @abstractmethod
    def get_active_ship(self) -> IShip:
        """This method provides the active ship"""


class ISetActiveShip(ABC):

    @abstractmethod
    def set_active_ship(self, ship: IShip) -> None:
        """This method sets the active ship based on user selection"""
