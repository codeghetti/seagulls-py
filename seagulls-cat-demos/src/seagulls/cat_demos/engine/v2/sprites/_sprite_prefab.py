from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import IExecutablePrefab
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from ._sprite_component import Sprite


class SpritePrefabRequest(NamedTuple):
    object_id: GameObjectId
    sprite: Sprite


class SpritePrefab(IExecutablePrefab[SpritePrefabRequest]):

    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def __call__(self, config: SpritePrefabRequest) -> None:
        # Sprite is the component config type
        component_id = GameComponentId[Sprite]("object-component::sprite")

        self._scene_objects.attach_component(
            entity_id=config.object_id,
            component_id=component_id,
        )

        component = self._scene_objects.open_component(
            entity_id=config.object_id,
            component_id=component_id,
        )
        component.set(config.sprite)
