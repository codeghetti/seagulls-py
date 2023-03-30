import logging
from abc import abstractmethod
from typing import Dict, Protocol, Set, Tuple

from ._game_objects import GameObjectId, IManageGameObjects
from ._object_components import GameComponentId, GameComponentType, ObjectComponentRegistry

logger = logging.getLogger(__name__)


class IManageGameObjectComponents(Protocol):

    @abstractmethod
    def attach_component(self, entity_id: GameObjectId, component_id: GameComponentId) -> None:
        pass

    @abstractmethod
    def detach_component(self, entity_id: GameObjectId, component_id: GameComponentId) -> None:
        pass


class SceneObjects(IManageGameObjects, IManageGameObjectComponents):

    _object_component_registry: ObjectComponentRegistry
    _entities: Dict[GameObjectId, Set[GameComponentId]]

    def __init__(self, object_component_registry: ObjectComponentRegistry) -> None:
        self._object_component_registry = object_component_registry
        self._entities = {}

    def add(self, entity_id: GameObjectId) -> None:
        if entity_id in self._entities:
            raise RuntimeError(f"duplicate entity found: {entity_id}")

        logger.warning(f"adding object to scene: {entity_id}")

        self._entities[entity_id] = set()

    def remove(self, entity_id: GameObjectId) -> None:
        if entity_id not in self._entities:
            raise RuntimeError(f"entity not found: {entity_id}")

        del self._entities[entity_id]

    def clear(self) -> None:
        self._entities.clear()

    def get(self) -> Tuple[GameObjectId, ...]:
        return tuple(self._entities.keys())

    def attach_component(self, entity_id: GameObjectId, component_id: GameComponentId) -> None:
        if entity_id not in self._entities:
            raise RuntimeError(f"entity not found: {entity_id}")

        if component_id in self._entities:
            raise RuntimeError(f"duplicate component found: {component_id}")

        self._entities[entity_id].add(component_id)
        self._object_component_registry.get(component_id).attach_object_component(entity_id)

    def detach_component(self, entity_id: GameObjectId, component_id: GameComponentId) -> None:
        if entity_id not in self._entities:
            raise RuntimeError(f"entity not found: {entity_id}")

        if component_id not in self._entities:
            raise RuntimeError(f"component not found: {component_id}")

        self._entities[entity_id].remove(component_id)
        self._object_component_registry.get(component_id).detach_object_component(entity_id)

    def get_component(
        self,
        entity_id: GameObjectId,
        component_id: GameComponentId[GameComponentType],
    ) -> GameComponentType:
        return self._object_component_registry.get(component_id).get_object_component(entity_id)
