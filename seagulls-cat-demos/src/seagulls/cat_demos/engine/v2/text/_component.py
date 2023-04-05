from __future__ import annotations

from typing import NamedTuple

import pygame

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.window._window import WindowClient


class Text(NamedTuple):
    value: str


class TextComponent:

    _objects: SceneObjects
    _window_client: WindowClient

    def __init__(self, objects: SceneObjects, window_client: WindowClient) -> None:
        self._objects = objects
        self._window_client = window_client

    def render_objects(self) -> None:
        for object_id in self._objects.find_by_component(GameComponentId[Text]("text.object-component")):
            text_component = self._objects.open_component(object_id, GameComponentId[Text]("text.object-component"))
            position_component = self._objects.open_component(
                object_id, GameComponentId[Position]("position.object-component"),
            )
            f = pygame.font.SysFont("monospace", 55)
            text = f.render(text_component.get().value, True, (80, 80, 200))
            surface = self._window_client.get_surface()
            surface.blit(text, position_component.get())
