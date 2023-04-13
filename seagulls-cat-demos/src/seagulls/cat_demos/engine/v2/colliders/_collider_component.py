from typing import NamedTuple, Tuple

from pygame import Rect

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import GamePrefabId, IExecutablePrefab
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import GameEvent, GameEventDispatcher, GameEventId
from seagulls.cat_demos.engine.v2.position._point import Position


class RectCollider(NamedTuple):
    size: Size


class CollisionEvent(NamedTuple):
    source_id: GameObjectId
    target_ids: Tuple[GameObjectId, ...]


class CollisionPrefab(IExecutablePrefab[GameObjectId]):

    _objects: SceneObjects
    _event_client: GameEventDispatcher

    def __init__(self, objects: SceneObjects, event_client: GameEventDispatcher) -> None:
        self._objects = objects
        self._event_client = event_client

    def __call__(self, source_id: GameObjectId) -> None:
        source_rect_collider = self._objects.get_component(
            source_id,
            GameComponentId[RectCollider]("object-component::rect-collider"),
        )
        source_position = self._objects.get_component(
            source_id,
            GameComponentId[Position]("object-component::position"),
        )
        source = Rect(source_position, source_rect_collider.size)
        targets = []
        target_ids = []

        for target_id in self._objects.find_by_component(GameComponentId[RectCollider]("object-component::rect-collider")):
            if target_id == source_id:
                continue

            target_rect_collider = self._objects.get_component(
                target_id,
                GameComponentId[RectCollider]("object-component::rect-collider"),
            )
            target_position = self._objects.get_component(
                target_id,
                GameComponentId[Position]("object-component::position"),
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
                GameEvent(
                    ColliderPrefabIds.COLLISION_EVENT,
                    CollisionEvent(source_id=source_id, target_ids=tuple(target_ids)),
                ),
            )


class ColliderPrefabIds:
    COLLISION_EVENT = GameEventId[CollisionEvent]("object-collisions")
    PREFAB = GamePrefabId[GameObjectId]("prefab::object-collisions")
    PREFAB_COMPONENT = GameComponentId[CollisionPrefab]("prefab::object-collisions")
