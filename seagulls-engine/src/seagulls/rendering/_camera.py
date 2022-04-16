import logging
from typing import Tuple

from seagulls.rendering import (
    Color,
    IClearPrinters,
    IPrintSquares,
    Position,
    Size
)
from seagulls.rendering._position import IUpdatePosition

logger = logging.getLogger(__name__)


class Camera(IPrintSquares, IClearPrinters, IUpdatePosition):

    _square_renderer: IPrintSquares
    _clearer: IClearPrinters
    _size: Size
    _position: Position
    _background_color: Color

    def __init__(
            self,
            square_renderer: IPrintSquares,
            clearer: IClearPrinters,
            size: Size,
            position: Position):
        self._square_renderer = square_renderer
        self._clearer = clearer
        self._size = size
        self._position = position

        self._background_color = Color({"r": 0, "g": 0, "b": 0})

    def print(self, color: Color, size: Size, position: Position):
        object_position = position.get()
        object_size = size.get()

        camera_position = self._position.get()
        camera_size = self._size.get()

        def _assert_objects_overlap() -> None:
            # This sounds like something we could do with collision detection
            if object_position["x"] + object_size["width"] < camera_position["x"]:
                # Object is too far to the left to be visible
                logger.warning("Object is too far to the left to be visible")
                raise ObjectDoesNotOverlapError()

            if object_position["y"] + object_size["height"] < camera_position["y"]:
                # Object is too far above to be visible
                logger.warning("Object is too far above to be visible")
                raise ObjectDoesNotOverlapError()

            if object_position["x"] > camera_position["x"] + camera_size["width"]:
                # Object is too far to the right to be visible
                logger.warning("# Object is too far to the right to be visible")
                raise ObjectDoesNotOverlapError()

            if object_position["y"] > camera_position["y"] + camera_size["height"]:
                # Object is too far below to be visible
                logger.warning("Object is too far below to be visible")
                raise ObjectDoesNotOverlapError()

        try:
            _assert_objects_overlap()
            adjusted_position = Position({
                "x": object_position["x"] - camera_position["x"],
                "y": object_position["y"] - camera_position["y"],
            })
            self._square_renderer.print(color, size, adjusted_position)
        except ObjectDoesNotOverlapError:
            logger.warning("Skipping!")
            pass

    def commit(self) -> None:
        self._square_renderer.commit()

    def clear(self):
        self._clearer.clear()

    def update_position(self, position: Position) -> None:
        self._position = position

    def move_position(self, direction: Tuple[int, int]) -> None:
        current = self._position.get()
        c_x = current["x"]
        c_y = current["y"]

        self._position = Position({
            "x": c_x + direction[0],
            "y": c_y + direction[1],
        })


class ObjectDoesNotOverlapError(Exception):
    """"""
