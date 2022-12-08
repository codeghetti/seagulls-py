from __future__ import annotations
from typing import NamedTuple, Tuple


class Position(NamedTuple):
    x: float
    y: float

    def __add__(self, other: Tuple[float, float]) -> "Position":
        return Position(x=other[0] + self.x, y=other[1] + self.y)


class PositionClient:

    _position: Position

    def __init__(self, position: Position) -> None:
        self._position = position

    def move(self, direction: Position) -> None:
        self._position += direction

    def get_position(self) -> Position:
        return self._position
