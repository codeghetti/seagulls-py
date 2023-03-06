from abc import abstractmethod
from typing import Any, Dict, Protocol, TypeAlias

from ._entities import EntityType, TypedEntityId
from ._game_objects import GameObjectId

GameComponentId: TypeAlias = TypedEntityId
GameComponentType: TypeAlias = EntityType


class GameComponentProvider(Protocol[GameComponentType]):

    @abstractmethod
    def __call__(self) -> GameComponentType:
        pass


class GameComponentRegistry:
    _providers: Dict[GameComponentId[Any], GameComponentProvider[Any]]

    def __init__(self) -> None:
        self._providers = {}

    def register(
        self,
        entity_id: GameComponentId[GameComponentType],
        provider: GameComponentProvider[GameComponentType],
    ) -> None:
        if entity_id in self._providers:
            raise RuntimeError(f"duplicate entity found: {entity_id}")

        self._providers[entity_id] = provider

    def get(self, entity_id: GameComponentId[GameComponentType]) -> GameComponentType:
        if entity_id not in self._providers:
            raise RuntimeError(f"entity not found: {entity_id}")

        return self._providers[entity_id]()


class IObjectComponentClient(Protocol[GameComponentType]):
    @abstractmethod
    def attach_object_component(self, game_object: GameObjectId) -> None:
        # Called when this component is added to a game object.
        pass

    @abstractmethod
    def detach_object_component(self, game_object: GameObjectId) -> None:
        # Called when this component is removed from a game object.
        pass

    @abstractmethod
    def get_object_component(self, game_object: GameObjectId) -> GameComponentType:
        pass


class ObjectComponentRegistry:

    _registry: GameComponentRegistry
    _providers: Dict[GameComponentId[Any], GameComponentId[IObjectComponentClient]]

    def __init__(self, registry: GameComponentRegistry) -> None:
        self._registry = registry
        self._components = {}

    def register(
        self,
        entity_id: GameComponentId[GameComponentType],
        provider: GameComponentId[IObjectComponentClient],
    ) -> None:
        if entity_id in self._components:
            raise RuntimeError(f"duplicate entity found: {entity_id}")

        self._components[entity_id] = provider

    def get(self, entity_id: GameComponentId[GameComponentType]) -> IObjectComponentClient[GameComponentType]:
        if entity_id not in self._components:
            print(self._components)
            raise RuntimeError(f"entity not found: {entity_id}")

        return self._registry.get(self._components[entity_id])
