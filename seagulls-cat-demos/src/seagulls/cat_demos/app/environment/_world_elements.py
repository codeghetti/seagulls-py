from enum import Enum
from typing import NamedTuple

from seagulls.cat_demos.engine.v2.collisions._collider_component import (
    RectCollider
)
from seagulls.cat_demos.engine.v2.components._component_containers import (
    GameComponentId
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import (
    GameComponentConfig,
    GameObjectConfig,
    GameObjectPrefab,
    GamePrefabId,
    IExecutablePrefab
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


class WorldElementPrefab(IExecutablePrefab[WorldElement]):
    _object_prefab: GameObjectPrefab

    def __init__(self, object_prefab: GameObjectPrefab) -> None:
        self._object_prefab = object_prefab

    def __call__(self, config: WorldElement) -> None:
        object_config = GameObjectConfig(
            object_id=config.object_id,
            components=(
                GameComponentConfig(
                    component_id=GameComponentId[Position](
                        "object-component::position"
                    ),
                    config=config.position,
                ),
                GameComponentConfig(
                    component_id=GameComponentId[Sprite]("object-component::sprite"),
                    config=Sprite(sprite_id=config.sprite_id.value),
                ),
                GameComponentConfig(
                    component_id=GameComponentId[RectCollider](
                        "object-component::rect-collider"
                    ),
                    config=RectCollider(size=Size(width=16, height=16)),
                ),
            ),
        )

        self._object_prefab(object_config)


class WorldElementIds:
    PREFAB = GamePrefabId[WorldElement]("prefab::world-element")
    PREFAB_COMPONENT = GameComponentId[WorldElementPrefab]("prefab::world-element")
