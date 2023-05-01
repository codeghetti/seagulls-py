from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._component_containers import (
    ObjectDataId
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import IPrefab
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from ._sprite_component import Sprite


class SpritePrefabRequest(NamedTuple):
    object_id: GameObjectId
    sprite: Sprite


class SpritePrefab(IPrefab[SpritePrefabRequest]):
    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def execute(self, request: SpritePrefabRequest) -> None:
        # Sprite is the component config type
        component_id = ObjectDataId[Sprite]("object-component::sprite")

        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=component_id,
            config=request.sprite,
        )
