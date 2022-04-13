from abc import abstractmethod
from typing import Protocol

from ._color import Color
from ._position import Position
from ._size import Size


class IPrintSquares(Protocol):

    @abstractmethod
    def print(self, color: Color, size: Size, position: Position) -> None:
        """"""

    @abstractmethod
    def commit(self) -> None:
        """"""


class IClearPrinters(Protocol):

    @abstractmethod
    def clear(self):
        """"""
