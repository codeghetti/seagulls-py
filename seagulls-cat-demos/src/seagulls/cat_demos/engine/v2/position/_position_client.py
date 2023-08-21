from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._object_data import ObjectDataId
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.position._point import Position


class PositionConfig(NamedTuple):
    object_id: GameObjectId
    position: Position


class PositionClient:
    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def execute(self, request: PositionConfig) -> None:
        component_id = ObjectDataId[Position]("position")

        self._scene_objects.set_data(
            object_id=request.object_id,
            data_id=component_id,
            config=request.position,
        )
