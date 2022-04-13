from abc import abstractmethod
from typing import Protocol

from pygame import Surface

from seagulls.rendering import SizeDict


class IProvideSurfaces(Protocol):

    @abstractmethod
    def get(self) -> Surface:
        """"""

    @abstractmethod
    def update(self, surface: Surface):
        """"""


class PygameSurface(IProvideSurfaces):

    _parent: IProvideSurfaces
    _size: SizeDict

    def __init__(self, parent: IProvideSurfaces, size: SizeDict):
        self._parent = parent
        self._size = size

    def get(self) -> Surface:
        return Surface((self._size["width"], self._size["height"]))

    def update(self, surface: Surface):
        self._parent.update(surface)
