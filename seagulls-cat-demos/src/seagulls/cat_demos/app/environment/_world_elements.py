from enum import Enum
from typing import NamedTuple

from seagulls.cat_demos.engine.v2.collisions._collision_client import (
    RectCollider, SelectionLayerId, SelectionLayers
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.position._point import Position
from seagulls.cat_demos.engine.v2.sprites._sprite_component import (
    Sprite,
    SpriteId
)


class WorldElementId(Enum):
    BARREL = SpriteId("barrel")
    CHEST_CLOSED = SpriteId("chest.closed")
    STAR_BACKGROUND = SpriteId("star_background")
    ROCK_LARGE = SpriteId("rock-large")


class WorldElement(NamedTuple):
    object_id: GameObjectId
    sprite_id: WorldElementId
    position: Position


class WorldElementClient:
    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def spawn(self, request: WorldElement) -> None:
        self._scene_objects.add(request.object_id)
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[Position]("position"),
            config=request.position,
        )
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[Sprite]("sprite"),
            config=Sprite(sprite_id=request.sprite_id.value, layer="environment"),
        )
        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=ObjectDataId[RectCollider]("rect-collider"),
            config=RectCollider(
                size=Size(width=16, height=16),
                layers=SelectionLayers(
                    appears_in=frozenset({SelectionLayerId("world-elements")}),
                    searches_in=frozenset({}),
                ),
            ),
        )


class WorldElementComponent:
    CLIENT_ID = ObjectDataId[WorldElementClient]("world-element-client")
