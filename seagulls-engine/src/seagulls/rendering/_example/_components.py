from pathlib import Path

from seagulls.pygame import PygamePrinter
from seagulls.rendering import Color, IPrinter, Position, Size
from seagulls.rendering._renderable_component import RenderableComponent
from seagulls.rendering._sprite import Sprite


class TextComponent(RenderableComponent):

    _text: str
    _font_path: Path
    _font_size: int
    _color: Color
    _size: Size
    _position: Position
    _printer: PygamePrinter

    def __init__(
            self,
            text: str,
            font_path: Path,
            font_size: int,
            color: Color,
            size: Size,
            position: Position,
            printer: PygamePrinter):
        self._text = text
        self._font_path = font_path
        self._font_size = font_size
        self._color = color
        self._size = size
        self._position = position
        self._printer = printer

    def render(self) -> None:
        self._printer.print_text(
            self._text,
            self._font_path,
            self._font_size,
            self._color,
            self._size,
            self._position,
        )


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

    _sprite: Sprite
    _size: Size
    _position: Position
    _printer: IPrinter

    def __init__(self, sprite: Sprite, size: Size, position: Position, printer: IPrinter):
        self._sprite = sprite
        self._size = size
        self._position = position
        self._printer = printer

    def render(self) -> None:
        self._printer.print_sprite(self._sprite, self._size, self._position)


class BoxComponent(RenderableComponent):

    _color: Color
    _size: Size
    _position: Position
    _printer: PygamePrinter

    def __init__(
            self,
            color: Color,
            size: Size,
            border_size: int,
            position: Position,
            printer: PygamePrinter):
        self._color = color
        self._size = size
        self._border_size = border_size
        self._position = position
        self._printer = printer

    def render(self) -> None:
        self._printer.print_box(self._color, self._size, self._border_size, self._position)
