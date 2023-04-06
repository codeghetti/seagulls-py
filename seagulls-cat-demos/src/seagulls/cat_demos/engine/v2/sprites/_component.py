from __future__ import annotations

from typing import NamedTuple

from pygame import Surface

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentContainer, GameComponentId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.window._window import WindowClient


class Sprite(NamedTuple):
    sprite_id: GameComponentId[Surface]
    size: int


class SpriteComponent:

    _objects: SceneObjects
    _container: GameComponentContainer
    _window_client: WindowClient

    def __init__(self, objects: SceneObjects, container: GameComponentContainer, window_client: WindowClient) -> None:
        self._objects = objects
        self._container = container
        self._window_client = window_client

    def render_objects(self) -> None:
        for object_id in self._objects.find_by_component(GameComponentId[Sprite]("sprite.object-component")):
            sprite_component = self._objects.open_component(
                object_id,
                GameComponentId[Sprite]("sprite.object-component"),
            )
            sprite_config = sprite_component.get()
            sprite_surface = self._container.get(sprite_config.sprite_id)

            position_component = self._objects.open_component(
                object_id,
                GameComponentId[Position]("position.object-component"),
            )
            surface = self._window_client.get_surface()
            surface.blit(sprite_surface, position_component.get())
