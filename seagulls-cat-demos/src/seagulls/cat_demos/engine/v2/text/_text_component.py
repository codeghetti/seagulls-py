from __future__ import annotations

import pygame
from functools import lru_cache
from pygame import Surface
from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.window._window import WindowClient


class Text(NamedTuple):
    value: str
    font: str
    size: int
    color: Color


class TextComponent(IExecutable):
    _objects: SceneObjects
    _window_client: WindowClient

    def __init__(self, objects: SceneObjects, window_client: WindowClient) -> None:
        self._objects = objects
        self._window_client = window_client

    def execute(self) -> None:
        for object_id in self._objects.find_by_data_id(
            ObjectDataId[Text]("text")
        ):
            text_component = self._objects.get_data(
                object_id, ObjectDataId[Text]("text")
            )
            position_component = self._objects.get_data(
                object_id,
                ObjectDataId[Position]("position"),
            )
            text = self._create_text(text_component)
            surface = self._window_client.get_layer("ui")
            surface.blit(text, position_component)

    @lru_cache()
    def _create_text(self, text: Text) -> Surface:
        f = pygame.font.SysFont(text.font, text.size)
        return f.render(text.value, True, text.color)
