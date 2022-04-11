import logging
from functools import lru_cache, cache

from pygame import Surface

from seagulls.rendering import (
    Color,
    IClearPrinters,
    IPrintSquares,
    Position,
    Size
)

from ._surface import IProvideSurfaces

logger = logging.getLogger(__name__)


class PygameSquarePrinter(IPrintSquares, IClearPrinters):

    _surface: IProvideSurfaces

    _copy: Surface

    def __init__(self, surface: IProvideSurfaces):
        self._surface = surface
        self._surface_cache_flag = True

    def render(self, color: Color, size: Size, position: Position):
        c = color.get()
        s = size.get()
        p = position.get()

        square = Surface((s["width"], s["height"]))
        square.fill((c["r"], c["g"], c["b"]))
        self._get_frame().blit(square, (p["x"], p["y"]))

    def clear(self) -> None:
        self._get_frame.cache_clear()

    @cache
    def _get_frame(self) -> Surface:
        frame = self._surface.get()
        frame.blit(self._get_copy(), (0, 0))
        return frame

    @cache
    def _get_copy(self) -> Surface:
        return self._surface.get().copy()
