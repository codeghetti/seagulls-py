from pygame import Rect
from typing import FrozenSet, NamedTuple, Tuple

from seagulls.cat_demos.engine.v2.components._entities import GameClientId, GameObjectId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.components._size import Size
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEvent,
    GameEventDispatcher,
    GameEventId
)
from seagulls.cat_demos.engine.v2.position._point import Position


class SelectionLayerId(NamedTuple):
    name: str


class SelectionLayers(NamedTuple):
    # Inspired by Godot's layers and masks
    appears_in: FrozenSet[SelectionLayerId]  # The layers this object appears in
    searches_in: FrozenSet[SelectionLayerId]  # The layers this object looks for collidables in


class RectCollider(NamedTuple):
    size: Size
    layers: SelectionLayers


class CollisionEvent(NamedTuple):
    source_id: GameObjectId
    target_ids: Tuple[GameObjectId, ...]


class CollisionClient:
    _objects: SceneObjects
    _event_client: GameEventDispatcher

    def __init__(
        self, objects: SceneObjects, event_client: GameEventDispatcher
    ) -> None:
        self._objects = objects
        self._event_client = event_client

    def check_collisions(self, source_id: GameObjectId) -> None:
        source_rect_collider = self._objects.get_data(
            source_id,
            ObjectDataId[RectCollider]("rect-collider"),
        )
        source_position = self._objects.get_data(
            source_id,
            ObjectDataId[Position]("position"),
        )
        source_layers = source_rect_collider.layers
        source = Rect(source_position, source_rect_collider.size)

        targets = []
        target_ids = []

        for target_id in self._objects.find_by_data_id(
            ObjectDataId[RectCollider]("rect-collider")
        ):
            if target_id == source_id:
                continue

            target_rect_collider = self._objects.get_data(
                target_id,
                ObjectDataId[RectCollider]("rect-collider"),
            )

            target_layers = target_rect_collider.layers
            target_appears_in_len = len(target_layers.appears_in)
            if len(target_layers.appears_in - source_layers.searches_in) == target_appears_in_len:
                # they don't appear in any layer we're searching, so we can't collide with them
                continue

            target_position = self._objects.get_data(
                target_id,
                ObjectDataId[Position]("position"),
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
                    id=CollisionComponent.COLLISION_EVENT,
                    payload=CollisionEvent(source_id=source_id, target_ids=tuple(target_ids)),
                ),
            )
            self._event_client.trigger(
                event=GameEvent(
                    id=CollisionComponent.object_collision_event(source_id),
                    payload=CollisionEvent(source_id=source_id, target_ids=tuple(target_ids)),
                ),
            )


class CollisionComponent:
    CLIENT_ID = GameClientId[CollisionClient]("collider-client")
    COLLISION_EVENT = GameEventId[CollisionEvent]("object-collisions")

    @staticmethod
    def object_collision_event(source_id: GameObjectId) -> GameEventId[CollisionEvent]:
        return GameEventId(f"object-collisions/{source_id.name}")
