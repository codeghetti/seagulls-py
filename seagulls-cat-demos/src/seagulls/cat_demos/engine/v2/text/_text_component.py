from __future__ import annotations

from functools import lru_cache
from typing import NamedTuple

import pygame
from pygame import Surface

from seagulls.cat_demos.engine.v2.components._color import Color
from seagulls.cat_demos.engine.v2.components._component_containers import (
    GameComponentId
)
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

    def __call__(self) -> None:
        for object_id in self._objects.find_by_component(
            GameComponentId[Text]("object-component::text")
        ):
            text_component = self._objects.get_component(
                object_id, GameComponentId[Text]("object-component::text")
            )
            position_component = self._objects.get_component(
                object_id,
                GameComponentId[Position]("object-component::position"),
            )
            text = self._create_text(text_component)
            surface = self._window_client.get_layer("ui")
            surface.blit(text, position_component)

    @lru_cache()
    def _create_text(self, text: Text) -> Surface:
        f = pygame.font.SysFont(text.font, text.size)
        return f.render(text.value, True, text.color)
