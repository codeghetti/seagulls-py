from __future__ import annotations

from typing import NamedTuple, Tuple


class Size(NamedTuple):
    height: float
    width: float

    def __add__(self, other: Tuple[float, float]) -> Size:
        return Size(height=self.height + other[0], width=self.width + other[1])

    def __sub__(self, other: Tuple[float, float]) -> Size:
        return Size(height=self.height - other[0], width=self.width - other[1])
