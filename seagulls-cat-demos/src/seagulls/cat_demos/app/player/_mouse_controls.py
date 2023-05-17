import logging
from datetime import datetime
from typing import NamedTuple, Set

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
from seagulls.cat_demos.engine.v2.scenes._scene_client import SceneContext

logger = logging.getLogger(__name__)


class MouseControls(NamedTuple):
    object_id: GameObjectId
    """
    The GameObjectId that we will update the position of.
    """


class MouseHoverEvent(NamedTuple):
    mouse_id: GameObjectId
    target_id: GameObjectId


class MouseClickEvent(NamedTuple):
    mouse_id: GameObjectId
    target_id: GameObjectId


class MouseControlClient:
    _scene_objects: SceneObjects
    _scene_context: SceneContext
    _event_client: GameEventDispatcher
    _collisions: CollisionClient

    def __init__(
        self,
        scene_objects: SceneObjects,
        scene_context: SceneContext,
        event_client: GameEventDispatcher,
        collisions: CollisionClient,
    ) -> None:
        self._scene_objects = scene_objects
        self._scene_context = scene_context
        self._event_client = event_client
        self._collisions = collisions

    def attach_mouse(self, request: MouseControls) -> None:

        this_frame: Set[GameObjectId] = set()
        active: Set[GameObjectId] = set()

        def on_collide() -> None:
            event = self._event_client.event()
            payload: CollisionEvent = event.payload
            source_id = payload.source_id
            target_ids = payload.target_ids
            if source_id != request.object_id:
                raise RuntimeError(f"this shouldn't happen: {source_id} != {request.object_id}")

            logger.debug(f"previously active: {active} ({datetime.now()})")

            for target in target_ids:
                this_frame.add(target)
                if target in active:
                    logger.debug(f"still hovering: {target} ({datetime.now()})")
                    self._event_client.trigger(GameEvent(
                        event_id=MouseControlComponent.target_hover_event(target),
                        payload=MouseHoverEvent(
                            mouse_id=source_id,
                            target_id=target,
                        ),
                    ))
                else:
                    logger.debug(f"newly hovering: {target} ({datetime.now()})")
                    self._event_client.trigger(GameEvent(
                        event_id=MouseControlComponent.target_mouse_enter_event(target),
                        payload=MouseHoverEvent(
                            mouse_id=source_id,
                            target_id=target,
                        ),
                    ))

        def on_mouse_move() -> None:
            this_frame.clear()
            event = self._event_client.event()
            payload: PygameMouseMotionEvent = event.payload
            self._scene_objects.set_data(
                object_id=request.object_id,
                data_id=ObjectDataId[Position]("position"),
                config=payload.position,
            )

            self._collisions.check_collisions(request.object_id)

            for candidate in active:
                if candidate not in this_frame:
                    # no longer hovering
                    self._event_client.trigger(GameEvent(
                        event_id=MouseControlComponent.target_mouse_exit_event(candidate),
                        payload=MouseHoverEvent(
                            mouse_id=request.object_id,
                            target_id=candidate,
                        ),
                    ))
                    logger.debug(f"no longer hovering: {candidate} ({datetime.now()})")

            active.clear()
            for active_object in this_frame:
                active.add(active_object)

        def on_mouse_press() -> None:
            for target_id in active:
                self._event_client.trigger(GameEvent(
                    event_id=MouseControlComponent.target_active_event(target_id),
                    payload=MouseClickEvent(
                        mouse_id=request.object_id,
                        target_id=target_id,
                    ),
                ))
                logger.debug(f"activated: {target_id} ({datetime.now()})")

        def on_mouse_release() -> None:
            for target_id in active:
                self._event_client.trigger(GameEvent(
                    event_id=MouseControlComponent.target_click_event(target_id),
                    payload=MouseClickEvent(
                        mouse_id=request.object_id,
                        target_id=target_id,
                    ),
                ))
                logger.debug(f"clicked: {target_id} ({datetime.now()})")

        self._event_client.register(
            PygameEvents.MOUSE_MOTION.namespace(self._scene_context.get().name),
            on_mouse_move,
        )
        self._event_client.register(
            PygameEvents.mouse_button_pressed(1).namespace(self._scene_context.get().name),
            on_mouse_press,
        )
        self._event_client.register(
            PygameEvents.MOUSE_BUTTON_RELEASED.namespace(self._scene_context.get().name),
            on_mouse_release,
        )
        self._event_client.register(
            CollisionComponent.object_collision_event(request.object_id),
            on_collide,
        )


class MouseControlComponent:
    CLIENT_ID = ObjectDataId[MouseControlClient]("mouse-control-client")

    @staticmethod
    def target_hover_event(target_id: GameObjectId) -> GameEventId[MouseHoverEvent]:
        """
        This event fires on each frame containing mouse movement events within the target colliders.
        """
        return GameEventId(f"mouse-hover/{target_id.name}")

    @staticmethod
    def target_mouse_enter_event(target_id: GameObjectId) -> GameEventId[MouseHoverEvent]:
        return GameEventId(f"mouse-enter/{target_id.name}")

    @staticmethod
    def target_mouse_exit_event(target_id: GameObjectId) -> GameEventId[MouseHoverEvent]:
        return GameEventId(f"mouse-exit/{target_id.name}")

    @staticmethod
    def target_active_event(target_id: GameObjectId) -> GameEventId[MouseClickEvent]:
        """
        The element is typically active when clicked down on but not yet released.
        """
        return GameEventId(f"mouse-active/{target_id.name}")

    @staticmethod
    def target_click_event(target_id: GameObjectId) -> GameEventId[MouseClickEvent]:
        return GameEventId(f"mouse-click/{target_id.name}")
