from abc import abstractmethod
from typing import Protocol, Tuple

from ._sprite import Sprite
from ._printer import IPrinter
from ._size import Size
from ._position import Position


class RenderableComponent(Protocol):
    @abstractmethod
    def render(self) -> None:
        """"""


class IProvideRenderables(Protocol):

    @abstractmethod
    def get(self) -> Tuple[RenderableComponent, ...]:
        """"""

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
