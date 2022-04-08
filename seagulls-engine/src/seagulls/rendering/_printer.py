from abc import abstractmethod
from typing import Protocol

from ._color import Color
from ._position import Position
from ._size import Size


class Printer(Protocol):

    @abstractmethod
    # Can we hide the rect detail here?
    def render(self, color: Color, size: Size, position: Position):
        """"""

    @abstractmethod
    def clear(self):
        """"""
