from __future__ import annotations

import pygame
from functools import lru_cache
from pygame import SRCALPHA, Surface
from typing import Dict, NamedTuple, Tuple, TypeAlias

from seagulls.cat_demos.engine.v2.components._entities import EntityId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.resources._resources_client import (
    ResourceClient
)
from seagulls.cat_demos.engine.v2.sessions._executables import IExecutable
from seagulls.cat_demos.engine.v2.window._window import WindowClient

SpriteId: TypeAlias = EntityId


class SpriteSource(NamedTuple):
    sprite_id: SpriteId
    image_name: str
    coordinates: Position
    size: Size


class Sprite(NamedTuple):
    sprite_id: SpriteId
    layer: str


class SpriteComponent(IExecutable):
    _objects: SceneObjects
    _window_client: WindowClient
    _resource_client: ResourceClient
    _sprite_sources: Dict[SpriteId, SpriteSource]

    def __init__(
        self,
        objects: SceneObjects,
        window_client: WindowClient,
        resource_client: ResourceClient,
        sprite_sources: Tuple[SpriteSource, ...],
    ) -> None:
        self._objects = objects
        self._window_client = window_client
        self._resource_client = resource_client
        self._sprite_sources = {source.sprite_id: source for source in sprite_sources}

    def execute(self) -> None:
        for object_id in self._objects.find_by_data_id(
            ObjectDataId[Sprite]("sprite")
        ):

            sprite_component = self._objects.get_data(
                object_id,
                ObjectDataId[Sprite]("sprite"),
            )
            sprite_surface = self._create_surface(
                self._sprite_sources[sprite_component.sprite_id]
            )

            position_component = self._objects.get_data(
                object_id,
                ObjectDataId[Position]("position"),
            )
            surface = self._window_client.get_layer(sprite_component.layer)
            surface.blit(sprite_surface, position_component)

    @lru_cache()
    def _create_surface(self, source: SpriteSource) -> Surface:
        path = self._resource_client.get_path(f"{source.image_name}.png")
        sprite_surface = pygame.image.load(path).convert_alpha()
        unit_surface = Surface(source.size, SRCALPHA, 32)
        unit_surface.blit(
            sprite_surface,
            Position(0, 0),
            (source.coordinates, source.size),
        )
        # scaled_surface = pygame.transform.scale(unit_surface, (s["width"], s["height"]))
        return unit_surface.copy()
