from typing import TypedDict


class ColorDict(TypedDict):
    r: int
    g: int
    b: int


class Color:

    _color: ColorDict

    def __init__(self, color: ColorDict):
        self._color = color

    def get(self) -> ColorDict:
        return self._color
