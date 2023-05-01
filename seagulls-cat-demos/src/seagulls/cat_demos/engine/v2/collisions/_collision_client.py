from pygame import Rect
from typing import NamedTuple, Tuple

from seagulls.cat_demos.engine.v2.components._component_containers import (
    ObjectDataId
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import (
    GamePrefabId,
    IPrefab
)
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEvent,
    GameEventDispatcher,
    GameEventId
)
from seagulls.cat_demos.engine.v2.position._point import Position


class RectCollider(NamedTuple):
    size: Size


class CollisionEvent(NamedTuple):
    source_id: GameObjectId
    target_ids: Tuple[GameObjectId, ...]


class CollisionClient(IPrefab[GameObjectId]):
    _objects: SceneObjects
    _event_client: GameEventDispatcher

    def __init__(
        self, objects: SceneObjects, event_client: GameEventDispatcher
    ) -> None:
        self._objects = objects
        self._event_client = event_client

    def execute(self, source_id: GameObjectId) -> None:
        source_rect_collider = self._objects.get_data(
            source_id,
            ObjectDataId[RectCollider]("object-component::rect-collider"),
        )
        source_position = self._objects.get_data(
            source_id,
            ObjectDataId[Position]("object-component::position"),
        )
        source = Rect(source_position, source_rect_collider.size)
        targets = []
        target_ids = []

        for target_id in self._objects.find_by_data_id(
            ObjectDataId[RectCollider]("object-component::rect-collider")
        ):
            if target_id == source_id:
                continue

            target_rect_collider = self._objects.get_data(
                target_id,
                ObjectDataId[RectCollider]("object-component::rect-collider"),
            )
            target_position = self._objects.get_data(
                target_id,
                ObjectDataId[Position]("object-component::position"),
            )

            # We need these two lists to be in sync :(
            targets.append(Rect(target_position, target_rect_collider.size))
            target_ids.append(target_id)

        indices = source.collidelistall(targets)
        collisions = []
        for i in indices:
            collisions.append(target_ids[i])

        if len(collisions) > 0:
            self._event_client.trigger(
                event=GameEvent(
                    id=ColliderPrefabIds.COLLISION_EVENT,
                    payload=CollisionEvent(source_id=source_id, target_ids=tuple(target_ids)),
                ),
            )


class ColliderPrefabIds:
    COLLISION_EVENT = GameEventId[CollisionEvent]("object-collisions")
    PREFAB = GamePrefabId[GameObjectId]("prefab::object-collisions")
    PREFAB_COMPONENT = ObjectDataId[CollisionClient]("prefab::object-collisions")
