from abc import abstractmethod
from typing import Generic, Protocol

from seagulls.cat_demos.engine.v2.components._component_containers import GameComponentId, \
    TypedGameComponentContainer
from seagulls.cat_demos.engine.v2.components._scene_objects import ComponentConfigType


class GamePrefabId(GameComponentId, Generic[ComponentConfigType]):
    pass


class PrefabProvider(Protocol[ComponentConfigType]):

    @abstractmethod
    def __call__(self, config: ComponentConfigType) -> None:
        pass


class PrefabClient:

    _container: TypedGameComponentContainer[PrefabProvider]

    def __init__(self, container: TypedGameComponentContainer[PrefabProvider]) -> None:
        self._container = container

    def run(self, prefab_id: GamePrefabId[ComponentConfigType], config: ComponentConfigType) -> None:
        self._container.get(GameComponentId(prefab_id.name))(config)
