from abc import abstractmethod
from typing import TypedDict, Protocol, Tuple


class PositionDict(TypedDict):
    x: int
    y: int


class Position:

    _position: PositionDict

    def __init__(self, position: PositionDict):
        self._position = position

    def get(self) -> PositionDict:
        return self._position


class IUpdatePosition(Protocol):

    @abstractmethod
    def update_position(self, position: Position) -> None:
        """"""

    @abstractmethod
    def move_position(self, direction: Tuple[int, int]) -> None:
        """"""
