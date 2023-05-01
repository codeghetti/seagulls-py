from abc import abstractmethod
from typing import Generic, NamedTuple, Protocol, Tuple, TypeAlias, TypeVar

from ._component_containers import ObjectDataId, TypedGameComponentContainer
from ._config_containers import T_GameConfigType, Tco_GameConfigType
from ._entities import GameObjectId
from ._scene_objects import SceneObjects

Tcontra_RequestType = TypeVar("Tcontra_RequestType", contravariant=True, bound=NamedTuple)
GamePrefabId: TypeAlias = ObjectDataId[Tco_GameConfigType]


class IPrefab(Protocol[Tcontra_RequestType]):
    @abstractmethod
    def execute(self, request: Tcontra_RequestType) -> None:
        pass


class PrefabClient:
    _container: TypedGameComponentContainer[IPrefab]

    def __init__(
        self, container: TypedGameComponentContainer[IPrefab]
    ) -> None:
        self._container = container

    def run(
        self, prefab_id: GamePrefabId[T_GameConfigType], config: T_GameConfigType
    ) -> None:
        self._container.get(ObjectDataId[T_GameConfigType](prefab_id.name)).execute(config)


class GameComponentConfig(NamedTuple, Generic[T_GameConfigType]):
    component_id: ObjectDataId[T_GameConfigType]
    config: T_GameConfigType


class GameObjectConfig(NamedTuple):
    object_id: GameObjectId
    components: Tuple[GameComponentConfig, ...]


class GameObjectPrefab(IPrefab[GameObjectConfig]):
    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def execute(self, request: GameObjectConfig) -> None:
        self._scene_objects.add(request.object_id)
        for component_config in request.components:
            self._scene_objects.set_data(
                entity_id=request.object_id,
                data_id=component_config.component_id,
                config=component_config.config,
            )
