from __future__ import annotations
from typing import Dict, NamedTuple, Tuple

from ._entities import GameObject


class Position(NamedTuple):
    x: float
    y: float

    def __add__(self, other: Tuple[float, float]) -> Position:
        return Position(x=self.x + other[0], y=self.y + other[1])

    def __sub__(self, other: Tuple[float, float]) -> Position:
        return Position(x=self.x - other[0], y=self.y - other[1])

    @staticmethod
    def zero() -> Position:
        return Position(0, 0)


class PositionComponent:
    _positions: Dict[GameObject: Position]

    def set_position(self, game_object: GameObject, position: Position) -> None:
        self._positions[game_object] = position

    def get_position(self, game_object: GameObject) -> Position:
        return self._positions.get(game_object, Position.zero())
