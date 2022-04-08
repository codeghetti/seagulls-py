from typing import TypedDict


class PositionDict(TypedDict):
    x: int
    y: int


class Position:

    _position: PositionDict

    def __init__(self, position: PositionDict):
        self._position = position

    def get(self) -> PositionDict:
        return self._position
