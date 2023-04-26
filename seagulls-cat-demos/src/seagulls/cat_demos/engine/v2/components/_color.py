from __future__ import annotations

from typing import NamedTuple, Tuple


class Color(NamedTuple):
    red: int
    green: int
    blue: int

    def __add__(self, other: Tuple) -> Color:
        return Color(
            red=self.red + other[0],
            green=self.green + other[1],
            blue=self.blue + other[2],
        )

    def __sub__(self, other: Tuple) -> Color:
        return Color(
            red=self.red - other[0],
            green=self.green - other[1],
            blue=self.blue - other[2],
        )
