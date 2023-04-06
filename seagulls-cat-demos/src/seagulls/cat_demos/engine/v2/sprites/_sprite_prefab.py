from typing import NamedTuple

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId
from seagulls.cat_demos.engine.v2.components._game_objects import GameObjectId
from seagulls.cat_demos.engine.v2.components._prefabs import PrefabProvider
from seagulls.cat_demos.engine.v2.components._scene_objects import SceneObjects
from seagulls.cat_demos.engine.v2.sprites._component import Sprite


class SpriteConfig(NamedTuple):
    object_id: GameObjectId
    sprite: Sprite


class SpritePrefab(PrefabProvider[SpriteConfig]):

    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def __call__(self, config: SpriteConfig) -> None:
        component_id = GameComponentId[Sprite]("sprite.object-component")

        self._scene_objects.attach_component(
            entity_id=config.object_id,
            component_id=component_id,
        )

        component = self._scene_objects.open_component(
            entity_id=config.object_id,
            component_id=component_id,
        )
        component.set(config.sprite)
