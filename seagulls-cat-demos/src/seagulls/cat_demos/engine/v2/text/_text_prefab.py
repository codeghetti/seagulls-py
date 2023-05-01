from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._component_containers import (
    ObjectDataId
)
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import IPrefab
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.text._text_component import Text


class TextConfig(NamedTuple):
    object_id: GameObjectId
    text: Text


class TextPrefab(IPrefab[TextConfig]):
    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def execute(self, request: TextConfig) -> None:
        component_id = ObjectDataId[Text]("object-component::text")

        self._scene_objects.set_data(
            entity_id=request.object_id,
            data_id=component_id,
            config=request.text,
        )
