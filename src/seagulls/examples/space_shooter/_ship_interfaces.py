import logging
from abc import ABC, abstractmethod

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


class IProvideActiveShip(ABC):

    @abstractmethod
    def get_active_ship(self) -> IShip:
        pass


class ISetActiveShip(ABC):

    @abstractmethod
    def set_active_ship(self, ship: IShip) -> None:
        pass
