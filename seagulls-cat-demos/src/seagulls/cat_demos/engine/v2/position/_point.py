from __future__ import annotations

from typing import NamedTuple, Tuple, TypeAlias


class Point(NamedTuple):
    x: float
    y: float

    def __add__(self, other: Tuple) -> Point:
        return Point(x=self.x + other[0], y=self.y + other[1])

    def __sub__(self, other: Tuple) -> Point:
        return Point(x=self.x - other[0], y=self.y - other[1])

    @classmethod
    def zero(cls) -> Point:
        return cls(0.0, 0.0)


Position: TypeAlias = Point
