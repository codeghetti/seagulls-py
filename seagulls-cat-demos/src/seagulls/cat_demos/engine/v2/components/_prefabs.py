from abc import abstractmethod
from typing import Generic, NamedTuple, Protocol, Tuple

from ._component_containers import GameComponentId, TypedGameComponentContainer
from ._config_containers import GameConfigType
from ._entities import GameObjectId
from ._scene_objects import SceneObjects


class GamePrefabId(GameComponentId, Generic[GameConfigType]):
    pass


class IExecutablePrefab(Protocol[GameConfigType]):

    @abstractmethod
    def __call__(self, config: GameConfigType) -> None:
        pass


class PrefabClient:

    _container: TypedGameComponentContainer[IExecutablePrefab]

    def __init__(self, container: TypedGameComponentContainer[IExecutablePrefab]) -> None:
        self._container = container

    def run(self, prefab_id: GamePrefabId[GameConfigType], config: GameConfigType) -> None:
        self._container.get(GameComponentId(prefab_id.name))(config)


class GameComponentConfig(NamedTuple):
    component_id: GameComponentId[GameConfigType]
    config: GameConfigType


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

            self._scene_objects.set_component(
                entity_id=config.object_id,
                component_id=component_config.component_id,
                config=component_config.config,
            )
