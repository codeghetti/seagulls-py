from abc import abstractmethod
from typing import Generic, NamedTuple, Protocol, Tuple

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId, \
    TypedGameComponentContainer
from seagulls.cat_demos.engine.v2.components._game_objects import GameObjectId
from seagulls.cat_demos.engine.v2.components._scene_objects import ComponentConfigType, SceneObjects


class GamePrefabId(GameComponentId, Generic[ComponentConfigType]):
    pass


class IExecutablePrefab(Protocol[ComponentConfigType]):

    @abstractmethod
    def __call__(self, config: ComponentConfigType) -> None:
        pass


class PrefabClient:

    _container: TypedGameComponentContainer[IExecutablePrefab]

    def __init__(self, container: TypedGameComponentContainer[IExecutablePrefab]) -> None:
        self._container = container

    def run(self, prefab_id: GamePrefabId[ComponentConfigType], config: ComponentConfigType) -> None:
        self._container.get(GameComponentId(prefab_id.name))(config)


class GameComponentConfig(NamedTuple):
    component_id: GameComponentId[ComponentConfigType]
    config: ComponentConfigType


class GameObjectConfig(NamedTuple):
    object_id: GameObjectId
    components: Tuple[GameComponentConfig, ...]


class GameObjectPrefab(IExecutablePrefab[GameObjectConfig]):

    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def __call__(self, config: GameObjectConfig) -> None:
        self._scene_objects.add(config.object_id)
        for component_config in config.components:
            self._scene_objects.attach_component(
                entity_id=config.object_id,
                component_id=component_config.component_id,
            )

            component = self._scene_objects.open_component(
                entity_id=config.object_id,
                component_id=component_config.component_id,
            )
            component.set(component_config.config)
