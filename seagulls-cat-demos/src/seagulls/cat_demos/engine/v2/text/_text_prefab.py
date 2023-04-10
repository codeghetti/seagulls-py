from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._entities import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import IExecutablePrefab
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.text._text_component import Text


class TextConfig(NamedTuple):
    object_id: GameObjectId
    text: Text


class TextPrefab(IExecutablePrefab[TextConfig]):

    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def __call__(self, config: TextConfig) -> None:
        component_id = GameComponentId[Text]("object-component::text")

        self._scene_objects.attach_component(
            entity_id=config.object_id,
            component_id=component_id,
        )

        component = self._scene_objects.open_component(
            entity_id=config.object_id,
            component_id=component_id,
        )
        component.set(config.text)
