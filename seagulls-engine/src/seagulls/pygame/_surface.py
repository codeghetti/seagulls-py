import logging
from abc import abstractmethod
from functools import cache
from typing import Protocol, Tuple

from pygame import Surface

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

    def __init__(
            self, parent: IProvideSurfaces,
            size: SizeDict):
        self._parent = parent
        self._size = size

    def get(self) -> Surface:
        return self._get_frame()

    def update(self, surface: Surface):
        logger.warning("update() in pygame surface (provider):")
        logger.warning(f"parent: {self._parent}")
        self._parent.update(surface)
        self._get_frame.cache_clear()

    @cache
    def _get_frame(self) -> Surface:
        logger.warning("get() in pygame surface (provider):")
        logger.warning(f"parent: {self._parent}")
        surface = Surface((self._size["width"], self._size["height"]))
        return surface
