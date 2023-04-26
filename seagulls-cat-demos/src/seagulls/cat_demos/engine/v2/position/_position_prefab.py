from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._component_containers import (
    GameComponentId
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import IExecutablePrefab
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.position._point import Position


class PositionConfig(NamedTuple):
    object_id: GameObjectId
    position: Position


class PositionPrefab(IExecutablePrefab[PositionConfig]):
    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def __call__(self, config: PositionConfig) -> None:
        component_id = GameComponentId[Position]("object-component::position")

        self._scene_objects.attach_component(
            entity_id=config.object_id,
            component_id=component_id,
        )
        self._scene_objects.set_component(
            entity_id=config.object_id,
            component_id=component_id,
            config=config.position,
        )
