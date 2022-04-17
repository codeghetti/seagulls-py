import logging
from pathlib import Path
from typing import Tuple

from seagulls.rendering import (
    Color,
    IPrintSquares,
    Position,
    Size, SizeDict
)
from seagulls.rendering._position import IUpdatePosition, PositionDict
from seagulls.rendering._printer import IPrintSprites

logger = logging.getLogger(__name__)


class Camera(IPrintSquares, IPrintSprites, IUpdatePosition):

    _square_printer: IPrintSquares
    _sprite_printer: IPrintSprites
    _size: Size
    _position: Position
    _background_color: Color

    def __init__(
            self,
            square_printer: IPrintSquares,
            sprite_printer: IPrintSprites,
            size: Size,
            position: Position):
        self._square_printer = square_printer
        self._sprite_printer = sprite_printer
        self._size = size
        self._position = position

        self._background_color = Color({"r": 60, "g": 0, "b": 0})

    def print_sprite(self, image_path: Path, size: Size, position: Position) -> None:
        logger.warning(f"Printing sprite! {image_path}")
        object_position = position.get()
        object_size = size.get()

        camera_position = self._position.get()

        try:
            self._assert_visible(object_position, object_size)
            adjusted_position = Position({
                "x": object_position["x"] - camera_position["x"],
                "y": object_position["y"] - camera_position["y"],
            })
            self._sprite_printer.print_sprite(image_path, size, adjusted_position)
            logger.warning(f"camera sprite printer: {self._sprite_printer}")
        except ObjectDoesNotOverlapError:
            pass

    def print_square(self, color: Color, size: Size, position: Position):
        object_position = position.get()
        object_size = size.get()

        camera_position = self._position.get()
        logger.warning(f"camera position: {self._position.get()}")
        logger.warning(f"object position: {object_position}")

        try:
            self._assert_visible(object_position, object_size)
            adjusted_position = Position({
                "x": object_position["x"] - camera_position["x"],
                "y": object_position["y"] - camera_position["y"],
            })
            logger.warning(f"square adjusted position: {adjusted_position.get()}")
            self._square_printer.print_square(color, size, adjusted_position)
        except ObjectDoesNotOverlapError:
            pass

    def commit(self) -> None:
        logger.warning(f"camera position: {self._position.get()}")
        self._sprite_printer.commit()
        self._square_printer.commit()

    def clear(self):
        self._sprite_printer.clear()
        self._square_printer.clear()
        self.print_square(self._background_color, self._size, self._position)

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

    def _assert_visible(self, object_position: PositionDict, object_size: SizeDict) -> None:
        camera_position = self._position.get()
        camera_size = self._size.get()

        # This sounds like something we could do with collision detection
        if object_position["x"] + object_size["width"] < camera_position["x"]:
            # Object is too far to the left to be visible
            raise ObjectDoesNotOverlapError()

        if object_position["y"] + object_size["height"] < camera_position["y"]:
            # Object is too far above to be visible
            raise ObjectDoesNotOverlapError()

        if object_position["x"] > camera_position["x"] + camera_size["width"]:
            # Object is too far to the right to be visible
            raise ObjectDoesNotOverlapError()

        if object_position["y"] > camera_position["y"] + camera_size["height"]:
            # Object is too far below to be visible
            raise ObjectDoesNotOverlapError()


class ObjectDoesNotOverlapError(Exception):
    """"""
