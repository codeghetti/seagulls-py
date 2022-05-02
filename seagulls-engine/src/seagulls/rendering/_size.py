from typing import TypedDict


class SizeDict(TypedDict):
    height: int
    width: int


class Size:

    _size: SizeDict

    def __init__(self, size: SizeDict):
        self._size = size

    def get(self) -> SizeDict:
        return self._size
