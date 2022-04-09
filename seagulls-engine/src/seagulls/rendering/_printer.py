from abc import abstractmethod
from typing import Protocol

from ._color import Color
from ._position import Position
from ._size import Size


class IPrintSquares(Protocol):

    @abstractmethod
    def render(self, color: Color, size: Size, position: Position):
        """"""


class IClearPrinters(Protocol):

    @abstractmethod
    def clear(self):
        """"""
