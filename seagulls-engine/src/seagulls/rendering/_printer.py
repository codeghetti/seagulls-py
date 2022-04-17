from abc import abstractmethod
from typing import Protocol

from ._color import Color
from ._position import Position
from ._size import Size


class IPrinter(Protocol):
    @abstractmethod
    def commit(self) -> None:
        """"""

    @abstractmethod
    def clear(self):
        """"""


class IPrintable(Protocol):
    @abstractmethod
    def print(self) -> None:
        """"""


class IPrintThings(IPrinter, Protocol):
    @abstractmethod
    def print(self, printable: IPrintable) -> None:
        """"""


class IPrintSquares(IPrinter, Protocol):

    @abstractmethod
    def print_square(self, color: Color, size: Size, position: Position) -> None:
        """"""


class PrintableSquare(IPrintable):
    _color: Color
    _size: Size
    _position: Position

    def print(self) -> None:
        """"""


"""
camera.print(player_sprite, (50, 50), (100, 25))
"""
