from pathlib import Path

from seagulls.rendering import Color, Size, Position, IPrinter
from seagulls.rendering._renderable_component import RenderableComponent


class SolidColorComponent(RenderableComponent):

    _color: Color
    _size: Size
    _position: Position
    _printer: IPrinter

    def __init__(self, color: Color, size: Size, position: Position, printer: IPrinter):
        self._color = color
        self._size = size
        self._position = position
        self._printer = printer

    def render(self) -> None:
        self._printer.print_square(self._color, self._size, self._position)


class SpriteComponent(RenderableComponent):

    _filepath: Path
    _size: Size
    _position: Position
    _printer: IPrinter

    def __init__(self, filepath: Path, size: Size, position: Position, printer: IPrinter):
        self._filepath = filepath
        self._size = size
        self._position = position
        self._printer = printer

    def render(self) -> None:
        self._printer.print_sprite(
            Path(f"../../../../{self._filepath}"), self._size, self._position)
