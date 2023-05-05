import logging
from typing import NamedTuple

from seagulls.cat_demos.engine.v2.collisions._collision_client import CollisionClient, \
    CollisionComponent, CollisionEvent
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEvent, GameEventDispatcher, GameEventId
)
from seagulls.cat_demos.engine.v2.input._pygame import (
    PygameEvents,
    PygameMouseMotionEvent
)
from seagulls.cat_demos.engine.v2.position._point import Position

logger = logging.getLogger(__name__)


class MouseControls(NamedTuple):
    object_id: GameObjectId
    """
    The GameObjectId that we will update the position of.
    """


class MouseHoverEvent(NamedTuple):
    mouse_id: GameObjectId
    target_id: GameObjectId


class MouseControlClient:
    _scene_objects: SceneObjects
    _event_client: GameEventDispatcher
    _collisions: CollisionClient

    def __init__(
        self,
        scene_objects: SceneObjects,
        event_client: GameEventDispatcher,
        collisions: CollisionClient,
    ) -> None:
        self._scene_objects = scene_objects
        self._event_client = event_client
        self._collisions = collisions

    def attach_mouse(self, request: MouseControls) -> None:
        def on_hover() -> None:
            event = self._event_client.event()
            payload: CollisionEvent = event.payload
            source_id = payload.source_id
            target_ids = payload.target_ids
            if source_id != request.object_id:
                raise RuntimeError(f"this shouldn't happen: {source_id} != {request.object_id}")

            for target_id in target_ids:
                # We shouldn't get multiple targets many times
                # But it's possible when objects overlap
                logger.warning(f"hovering {source_id} -> {target_id}")
                self._event_client.trigger(GameEvent(
                    id=MouseControlComponent.target_hover_event(target_id),
                    payload=MouseHoverEvent(
                        mouse_id=source_id,
                        target_id=target_id,
                    ),
                ))

        def on_mouse() -> None:
            event = self._event_client.event()
            payload: PygameMouseMotionEvent = event.payload
            self._scene_objects.set_data(
                object_id=request.object_id,
                data_id=ObjectDataId[Position]("position"),
                config=payload.position,
            )

            self._collisions.check_collisions(request.object_id)

        self._event_client.register(PygameEvents.MOUSE_MOTION, on_mouse)
        self._event_client.register(
            CollisionComponent.object_collision_event(request.object_id),
            on_hover,
        )


class MouseControlComponent:
    CLIENT_ID = ObjectDataId[MouseControlClient]("mouse-control-client")

    @staticmethod
    def target_hover_event(target_id: GameObjectId) -> GameEventId[MouseHoverEvent]:
        return GameEventId(f"mouse-hover/{target_id.name}")
