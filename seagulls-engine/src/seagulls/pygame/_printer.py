from pygame import Surface

from seagulls.rendering import (
    Color,
    IClearPrinters,
    IPrintSquares,
    Position,
    Size
)

from ._surface import IProvideSurfaces


class PygameSquarePrinter(IPrintSquares, IClearPrinters):

    _surface: IProvideSurfaces

    def __init__(self, surface: IProvideSurfaces):
        self._surface = surface

    def render(self, color: Color, size: Size, position: Position):
        c = color.get()
        s = size.get()
        p = position.get()

        square = Surface((s["width"], s["height"]))
        square.fill((c["r"], c["g"], c["b"]))
        self._surface.get().blit(square, (p["x"], p["y"]))

    def clear(self) -> None:
        self._surface.get().fill((0, 0, 0))
