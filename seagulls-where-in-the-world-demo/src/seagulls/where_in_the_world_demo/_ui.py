from typing import NamedTuple

from pygame import Surface


class PixelUi(NamedTuple):
    bullet_orange: Surface
    bullet_yellow: Surface
    bullet_green: Surface
    bullet_white: Surface
    bullet_grey: Surface

    panel_top_left_dark_brown: Surface
    panel_top_dark_brown: Surface
    panel_top_right_dark_brown: Surface
    panel_left_dark_brown: Surface
    panel_center_dark_brown: Surface
    panel_right_dark_brown: Surface
    panel_bottom_left_dark_brown: Surface
    panel_bottom_dark_brown: Surface
    panel_bottom_right_dark_brown: Surface

    panel_top_left_light_brown: Surface
    panel_top_light_brown: Surface
    panel_top_right_light_brown: Surface
    panel_left_light_brown: Surface
    panel_center_light_brown: Surface
    panel_right_light_brown: Surface
    panel_bottom_left_light_brown: Surface
    panel_bottom_light_brown: Surface
    panel_bottom_right_light_brown: Surface

    panel_top_left_light_grey: Surface
    panel_top_light_grey: Surface
    panel_top_right_light_grey: Surface
    panel_left_light_grey: Surface
    panel_center_light_grey: Surface
    panel_right_light_grey: Surface
    panel_bottom_left_light_grey: Surface
    panel_bottom_light_grey: Surface
    panel_bottom_right_light_grey: Surface


class BoxSurfaces(NamedTuple):
    top_left: Surface
    top: Surface
    top_right: Surface
    left: Surface
    center: Surface
    right: Surface
    bottom_left: Surface
    bottom: Surface
    bottom_right: Surface
