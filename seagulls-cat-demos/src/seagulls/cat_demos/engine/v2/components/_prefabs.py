from abc import abstractmethod
from typing import Generic, Protocol, Tuple, TypeAlias, TypeVar

from typing_extensions import NamedTuple

from ._component_containers import GameComponentId, TypedGameComponentContainer
from ._config_containers import T_GameConfigType, Tco_GameConfigType
from ._entities import GameObjectId
from ._scene_objects import SceneObjects

T = TypeVar("T")
T_contra = TypeVar("T_contra", contravariant=True)
GamePrefabId: TypeAlias = GameComponentId[Tco_GameConfigType]


class IExecutablePrefab(Protocol[T_contra]):

    @abstractmethod
    def __call__(self, config: T_contra) -> None:
        pass


class PrefabClient:

    _container: TypedGameComponentContainer[IExecutablePrefab]

    def __init__(self, container: TypedGameComponentContainer[IExecutablePrefab]) -> None:
        self._container = container

    def run(self, prefab_id: GamePrefabId[T_GameConfigType], config: T_GameConfigType) -> None:
        self._container.get(GameComponentId(prefab_id.name))(config)


class GameComponentConfig(NamedTuple, Generic[T_GameConfigType]):
    component_id: GameComponentId[T_GameConfigType]
    config: T_GameConfigType


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
