from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._component_containers import (
    ObjectDataId
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import (
    GamePrefabId,
    IPrefab
)
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.eventing._event_dispatcher import (
    GameEventDispatcher
)
from seagulls.cat_demos.engine.v2.input._pygame import (
    PygameEvents,
    PygameMouseMotionEvent
)
from seagulls.cat_demos.engine.v2.position._point import Position


class MouseControls(NamedTuple):
    object_id: GameObjectId
    """
    The GameObjectId that we will update the position of.
    """


class MouseControlsPrefab(IPrefab[MouseControls]):
    _scene_objects: SceneObjects
    _event_client: GameEventDispatcher

    def __init__(
        self,
        scene_objects: SceneObjects,
        event_client: GameEventDispatcher,
    ) -> None:
        self._scene_objects = scene_objects
        self._event_client = event_client

    def execute(self, request: MouseControls) -> None:
        def on_mouse() -> None:
            event = self._event_client.event()
            payload: PygameMouseMotionEvent = event.payload
            self._scene_objects.set_data(
                entity_id=request.object_id,
                data_id=ObjectDataId[Position]("object-component::position"),
                config=payload.position,
            )

        self._event_client.register(PygameEvents.MOUSE_MOTION, on_mouse)


class MouseControlIds:
    PREFAB = GamePrefabId[MouseControls]("prefab::mouse-controls")
    PREFAB_COMPONENT = ObjectDataId[MouseControlsPrefab]("prefab::mouse-controls")
