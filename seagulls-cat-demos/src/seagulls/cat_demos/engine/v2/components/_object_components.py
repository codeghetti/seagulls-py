from abc import abstractmethod
from typing import Any, Dict, Protocol

from ._component_registry import GameComponentFactory, GameComponentId, GameComponentType
from ._game_objects import GameObjectId


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

    _registry: GameComponentFactory
    _providers: Dict[GameComponentId[Any], GameComponentId[IObjectComponentClient]]

    def __init__(self, registry: GameComponentFactory) -> None:
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

        return self._registry.create(self._components[entity_id])
