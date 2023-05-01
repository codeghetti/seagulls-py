from enum import Enum
from typing import NamedTuple

from seagulls.cat_demos.engine.v2.collisions._collision_client import (
    RectCollider
)
from seagulls.cat_demos.engine.v2.components._component_containers import (
    ObjectDataId
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import (
    GameComponentConfig,
    GameObjectConfig,
    GameObjectPrefab
)
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
    _object_prefab: GameObjectPrefab

    def __init__(self, object_prefab: GameObjectPrefab) -> None:
        self._object_prefab = object_prefab

    def spawn(self, request: WorldElement) -> None:
        object_config = GameObjectConfig(
            object_id=request.object_id,
            components=(
                GameComponentConfig(
                    component_id=ObjectDataId[Position](
                        "object-component::position"
                    ),
                    config=request.position,
                ),
                GameComponentConfig(
                    component_id=ObjectDataId[Sprite]("object-component::sprite"),
                    config=Sprite(sprite_id=request.sprite_id.value, layer="environment"),
                ),
                GameComponentConfig(
                    component_id=ObjectDataId[RectCollider](
                        "object-component::rect-collider"
                    ),
                    config=RectCollider(size=Size(width=16, height=16)),
                ),
            ),
        )

        self._object_prefab.execute(object_config)


class WorldElementIds:
    CLIENT_ID = ObjectDataId[WorldElementClient]("world-element-client")
