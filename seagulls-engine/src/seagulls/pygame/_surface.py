import logging
from abc import abstractmethod
from typing import Protocol, Tuple

from pygame import SRCALPHA

from seagulls.engine import Surface
from seagulls.rendering import SizeDict

logger = logging.getLogger(__name__)


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
    _background_color: Tuple[int, int, int]

    def __init__(
            self, parent: IProvideSurfaces,
            size: SizeDict,
            background_color: Tuple[int, int, int]):
        self._parent = parent
        self._size = size
        self._background_color = background_color

    def get(self) -> Surface:
        surface = Surface((self._size["width"], self._size["height"]), SRCALPHA, 32)
        surface.fill(self._background_color)
        return surface

    def update(self, surface: Surface):
        self._parent.update(surface)
