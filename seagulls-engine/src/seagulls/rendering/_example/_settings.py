from dataclasses import dataclass

from seagulls.pygame import WindowSurface
from seagulls.rendering import SizeDict


class MyResolutionSettings:
    _window: WindowSurface

    def __init__(self, window: WindowSurface):
        self._window = window


@dataclass(frozen=True)
class VideoSettings:
    window_size: SizeDict
    scene_size: SizeDict
    camera_size: SizeDict
