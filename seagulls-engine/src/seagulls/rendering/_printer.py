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


class IPrintSquares(IPrinter, Protocol):

    @abstractmethod
    def print_square(self, color: Color, size: Size, position: Position) -> None:
        """"""
