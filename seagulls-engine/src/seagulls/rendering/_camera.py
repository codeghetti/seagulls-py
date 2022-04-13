import logging

import pygame

from seagulls.rendering import (
    Color,
    IClearPrinters,
    IPrintSquares,
    Position,
    Size
)

logger = logging.getLogger(__name__)


class Camera(IPrintSquares, IClearPrinters):

    _square_renderer: IPrintSquares
    _clearer: IClearPrinters
    _size: Size
    _resolution: Size
    _position: Position

    def __init__(
            self,
            square_renderer: IPrintSquares,
            clearer: IClearPrinters,
            size: Size,
            resolution: Size,
            position: Position):
        self._square_renderer = square_renderer
        self._clearer = clearer
        self._size = size
        self._resolution = resolution
        self._position = position

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
            self._square_renderer.print(
                color,
                self._adjust_size(size),
                self._adjust_position(position))
        except ObjectDoesNotOverlapError:
            logger.warning("Skipping!")
            pass

    def _adjust_position(self, position: Position) -> Position:
        if self._size == self._resolution:
            # No adjustments needed
            return position

        posdict = position.get()
        camdizedict = self._size.get()
        resdict = self._resolution.get()

        camera_aspect_ratio = self._size.get()["height"] / self._size.get()["width"]
        # ratio of our camera height to resolution height
        rh_ratio = camdizedict["height"] / resdict["height"]
        # ratio of our camera width to resolution width
        rw_ratio = camdizedict["width"] / resdict["width"]
        screen_aspect_ratio = resdict["height"] / resdict["width"]

        logger.warning(f"posdict: {posdict}")
        logger.warning(f"camdizedict: {camdizedict}")
        logger.warning(f"resdict: {resdict}")
        logger.warning(f"rh_ratio: {rh_ratio}")
        logger.warning(f"rw_ratio: {rw_ratio}")
        logger.warning(f"camera_aspect_ratio: {camera_aspect_ratio}")
        logger.warning(f"screen_aspect_ratio: {screen_aspect_ratio}")

        """
        window_size={"height": 1000, "width": 1200},
        scene_size={"height": 500, "width": 500},
        camera_size={"height": 500, "width": 500},
        """

        x_padding = 0
        y_padding = 0

        if camera_aspect_ratio == screen_aspect_ratio:
            adjusted_x = int(posdict["x"] / rw_ratio)
            adjusted_y = int(posdict["y"] / rh_ratio)
        elif camera_aspect_ratio > screen_aspect_ratio:
            # screen is wider than our camera can display
            adjusted_camera_size = {
                "height": camdizedict["height"] / rh_ratio,
                "width": camdizedict["width"] / rh_ratio,
            }
            adjusted_x = int(posdict["x"] / rh_ratio)
            adjusted_y = int(posdict["y"] / rh_ratio)

            x_padding = int((resdict["width"] - adjusted_camera_size["width"]) / 2)
        else:
            # screen is taller than our camera can display
            adjusted_camera_size = {
                "height": camdizedict["height"] / rw_ratio,
                "width": camdizedict["width"] / rw_ratio,
            }
            adjusted_x = int(posdict["x"] / rw_ratio)
            adjusted_y = int(posdict["y"] / rw_ratio)

            y_padding = int((resdict["height"] - adjusted_camera_size["height"]) / 2)

        logger.warning(f"x_padding: {x_padding}")
        logger.warning(f"y_padding: {y_padding}")

        adjusted_position = Position({
            "x": x_padding + adjusted_x,
            "y": y_padding + adjusted_y,
        })
        logger.warning(
            f"adjusted_position: {posdict} -> {adjusted_position.get()}")

        return adjusted_position

    def _adjust_size(self, size: Size) -> Size:
        if self._size == self._resolution:
            # No adjustments needed
            return size

        sizedict = size.get()
        camdict = self._size.get()
        resdict = self._resolution.get()

        camera_aspect_ratio = self._size.get()["height"] / self._size.get()["width"]
        # ratio of our camera height to resolution height
        rh_ratio = camdict["height"] / resdict["height"]
        # ratio of our camera width to resolution width
        rw_ratio = camdict["width"] / resdict["width"]
        screen_aspect_ratio = resdict["height"] / resdict["width"]

        logger.warning(f"camdict: {camdict}")
        logger.warning(f"resdict: {resdict}")
        logger.warning(f"rh_ratio: {rh_ratio}")
        logger.warning(f"rw_ratio: {rw_ratio}")
        logger.warning(f"camera_aspect_ratio: {camera_aspect_ratio}")
        logger.warning(f"screen_aspect_ratio: {screen_aspect_ratio}")

        """
        window_size={"height": 1000, "width": 1200},
        scene_size={"height": 500, "width": 500},
        camera_size={"height": 500, "width": 500},
        """

        if camera_aspect_ratio == screen_aspect_ratio:
            adjusted_width = int(sizedict["width"] / rw_ratio)
            adjusted_height = int(sizedict["height"] / rh_ratio)
        elif camera_aspect_ratio > screen_aspect_ratio:
            # screen is wider than our camera can display
            adjusted_width = int(sizedict["width"] / rh_ratio)
            adjusted_height = int(sizedict["height"] / rh_ratio)
        else:
            # screen is taller than our camera can display
            adjusted_width = int(sizedict["width"] / rw_ratio)
            adjusted_height = int(sizedict["height"] / rw_ratio)

        adjusted_size = Size({
            "width": adjusted_width,
            "height": adjusted_height,
        })
        logger.warning(
            f"adjusted_size: {sizedict} -> {adjusted_size.get()}")

        return adjusted_size

    def commit(self) -> None:
        self._square_renderer.commit()

    def clear(self):
        self._clearer.clear()


class ObjectDoesNotOverlapError(Exception):
    """"""
