from abc import abstractmethod
from pathlib import Path
from typing import Protocol

from ._color import Color
from ._position import Position
from ._size import Size


class IPrinter(Protocol):

    @abstractmethod
    def print_square(self, color: Color, size: Size, position: Position) -> None:
        """"""

    @abstractmethod
    def print_sprite(self, file: Path, size: Size, position: Position) -> None:
        """"""

    @abstractmethod
    def commit(self) -> None:
        """"""

    @abstractmethod
    def clear(self):
        """"""


"""
camera.print(player_sprite, (50, 50), (100, 25))
"""
