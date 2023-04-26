from __future__ import annotations

from typing import NamedTuple, Tuple


class Size(NamedTuple):
    width: int
    height: int

    def __add__(self, other: Tuple) -> Size:
        return Size(height=self.height + other[0], width=self.width + other[1])

    def __sub__(self, other: Tuple) -> Size:
        return Size(height=self.height - other[0], width=self.width - other[1])
