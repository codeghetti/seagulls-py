import logging
from abc import abstractmethod
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
    _background_color: Tuple[int, int, int]

    def __init__(
            self, parent: IProvideSurfaces,
            size: SizeDict,
            background_color: Tuple[int, int, int]):
        self._parent = parent
        self._size = size
        self._background_color = background_color

    def get(self) -> Surface:
        surface = Surface((self._size["width"], self._size["height"]))
        surface.fill(self._background_color)
        return surface

    def update(self, surface: Surface):
        self._parent.update(surface)


class DeferredPygameSurface(IProvideSurfaces):

    _parent: IProvideSurfaces

    def __init__(self, parent: IProvideSurfaces):
        self._parent = parent

    def get(self) -> Surface:
        return self._parent.get()

    def update(self, surface: Surface):
        logger.warning(f"deferred update called")
        self._parent.update(surface)
        # self._parent.get().blit(surface, (0, 0))

    def end_frame(self) -> None:
        logger.warning(f"deferred end frame called")
        # self._parent.update(self._parent.get())
