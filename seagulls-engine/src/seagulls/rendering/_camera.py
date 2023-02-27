import logging
from typing import Tuple

from ._position import IUpdatePosition, Position
from ._size import Size

logger = logging.getLogger(__name__)


class Camera(IUpdatePosition):

    """
    2022-04-16
    New Camera Idea:
    - Camera is not a printer
    - Store all the `print` operations in a list
    - Filter the `print` operations based on camera position + size
    - On `commit`, forward the operations to a `real` printer
    - end the frame?
    """

    _size: Size
    _position: Position

    def __init__(
            self,
            size: Size,
            position: Position):
        self._size = size
        self._position = position

    def adjust_position(self, original: Position) -> Position:
        object_position = original.get()
        camera_position = self._position.get()

        return Position({
            "x": object_position["x"] - camera_position["x"],
            "y": object_position["y"] - camera_position["y"],
        })

    def relative_position(self, original: Position) -> Position:
        object_position = original.get()
        camera_position = self._position.get()

        return Position({
            "x": object_position["x"] + camera_position["x"],
            "y": object_position["y"] + camera_position["y"],
        })

    def assert_visible(self, size: Size, position: Position) -> None:
        object_position = position.get()
        object_size = size.get()

        camera_position = self._position.get()
        camera_size = self._size.get()

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
