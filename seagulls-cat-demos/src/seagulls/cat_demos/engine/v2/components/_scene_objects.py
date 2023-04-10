import logging
from typing import Any, Dict, Generic, Set, Tuple

from ._component_containers import GameComponentContainer, GameComponentId, TypedGameComponentContainer
from ._config_containers import GameConfigType
from ._entities import GameObjectId
from ._service_provider import ServiceProvider

logger = logging.getLogger(__name__)


class ObjectComponent(Generic[GameConfigType]):

    _context: ServiceProvider[GameObjectId]
    _configs: Dict[GameObjectId, GameConfigType]

    def __init__(
        self,
        context: ServiceProvider[GameObjectId],
    ) -> None:
        self._context = context
        self._configs = {}

    def get(self) -> GameConfigType:
        return self._configs[self._context()]

    def set(self, config: GameConfigType) -> None:
        self._configs[self._context()] = config


class SceneObjects:

    _container: TypedGameComponentContainer[ObjectComponent]
    _entities: Dict[GameObjectId, Set[GameComponentId]]
    _components: Dict[GameComponentId[Any], Dict[GameObjectId, ObjectComponent[Any]]]

    def __init__(self, container: GameComponentContainer) -> None:
        self._container = container
        self._entities = {}
        self._components = {}

    def add(self, entity_id: GameObjectId) -> None:
        if entity_id in self._entities:
            raise RuntimeError(f"duplicate entity found: {entity_id}")

        self._entities[entity_id] = set()

    def remove(self, entity_id: GameObjectId) -> None:
        if entity_id not in self._entities:
            raise RuntimeError(f"entity not found: {entity_id}")

        del self._entities[entity_id]

    def get(self) -> Tuple[GameObjectId, ...]:
        return tuple(self._entities.keys())

    def attach_component(self, entity_id: GameObjectId, component_id: GameComponentId) -> None:
        if entity_id not in self._entities:
            raise RuntimeError(f"entity not found: {entity_id}")

        if component_id in self._entities[entity_id]:
            raise RuntimeError(f"duplicate component found: {component_id}")

        self._entities[entity_id].add(component_id)

        if component_id not in self._components:
            self._components[component_id] = {}
        self._components[component_id][entity_id] = ObjectComponent(context=lambda: entity_id)

    def detach_component(self, entity_id: GameObjectId, component_id: GameComponentId) -> None:
        if entity_id not in self._entities:
            raise RuntimeError(f"entity not found: {entity_id}")

        if component_id not in self._entities:
            raise RuntimeError(f"component not found: {component_id}")

        self._entities[entity_id].remove(component_id)

    def set_component(
            self,
            entity_id: GameObjectId,
            component_id: GameComponentId[GameConfigType],
            config: GameConfigType,
    ) -> None:
        self._components[component_id][entity_id].set(config)

    def get_component(
            self,
            entity_id: GameObjectId,
            component_id: GameComponentId[GameConfigType],
    ) -> GameConfigType:
        return self._components[component_id][entity_id].get()

    def find_by_component(self, component_id: GameComponentId) -> Tuple[GameObjectId, ...]:
        result = []
        for e, cs in self._entities.items():
            if component_id in cs:
                result.append(e)

        return tuple(result)
