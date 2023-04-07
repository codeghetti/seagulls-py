from __future__ import annotations

from typing import NamedTuple

import pygame
from pygame import SRCALPHA, Surface

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.resources._resources_client import ResourceClient
from seagulls.cat_demos.engine.v2.sprites._sprite_container import SpriteContainer
from seagulls.cat_demos.engine.v2.window._window import WindowClient


class SpriteSource(NamedTuple):
    image_name: str
    coordinates: Position
    size: Size


class Sprite(NamedTuple):
    sprite_id: GameComponentId[Surface]


class SpriteComponent:

    _objects: SceneObjects
    _container: SpriteContainer
    _window_client: WindowClient
    _resource_client: ResourceClient

    def __init__(
        self,
        objects: SceneObjects,
        container: SpriteContainer,
        window_client: WindowClient,
        resource_client: ResourceClient
    ) -> None:
        self._objects = objects
        self._container = container
        self._window_client = window_client
        self._resource_client = resource_client

    def create_surface(self, source: SpriteSource) -> Surface:
        path = self._resource_client.get_path(f"{source.image_name}.png")
        sprite_surface = pygame.image.load(path).convert_alpha()
        unit_surface = Surface(source.size, SRCALPHA, 32)
        unit_surface.blit(
            sprite_surface,
            Position(0, 0),
            (source.coordinates.x, source.coordinates.y, source.size.width, source.size.height),
        )
        # scaled_surface = pygame.transform.scale(unit_surface, (s["width"], s["height"]))
        return unit_surface

    def render_objects(self) -> None:
        for object_id in self._objects.find_by_component(GameComponentId[Sprite]("object-component::sprite")):
            sprite_component = self._objects.open_component(
                object_id,
                GameComponentId[Sprite]("object-component::sprite"),
            )
            sprite_config = sprite_component.get()
            sprite_surface = self._container.get(sprite_config.sprite_id)

            position_component = self._objects.open_component(
                object_id,
                GameComponentId[Position]("object-component::position"),
            )
            surface = self._window_client.get_surface()
            surface.blit(sprite_surface, position_component.get())
