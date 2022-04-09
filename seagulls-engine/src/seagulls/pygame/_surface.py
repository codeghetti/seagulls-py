from abc import abstractmethod
from typing import Protocol

from pygame import Surface


class IProvideSurfaces(Protocol):

    @abstractmethod
    def get(self) -> Surface:
        """"""
