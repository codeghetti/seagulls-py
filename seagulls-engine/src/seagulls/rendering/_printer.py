from abc import abstractmethod
from pathlib import Path
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


class IPrintSprites(IPrinter, Protocol):

    @abstractmethod
    def print_sprite(self, image_path: Path, size: Size, position: Position) -> None:
        """"""


class IPrintSquares(IPrinter, Protocol):

    @abstractmethod
    def print_square(self, color: Color, size: Size, position: Position) -> None:
        """"""
