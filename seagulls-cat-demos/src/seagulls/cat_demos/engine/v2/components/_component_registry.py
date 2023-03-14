from abc import abstractmethod
from typing import Any, Dict, Protocol, Tuple

from seagulls.cat_demos.engine.v2.components._entities import EntityType, TypedEntityId


class GameComponentId(TypedEntityId[EntityType]):
    pass


class GameComponentType(EntityType):
    pass


class GameComponentProvider(Protocol[GameComponentType]):

    @abstractmethod
    def __call__(self) -> GameComponentType:
        pass


class GameComponentRegistry:

    _providers: Dict[GameComponentId[Any], GameComponentProvider[Any]]

    @staticmethod
    def with_providers(
            *provider: Tuple[GameComponentId[GameComponentType], GameComponentProvider[GameComponentType]]
    ) -> "GameComponentRegistry":
        i = GameComponentRegistry()
        for p in provider:
            i.register(p[0], p[1])
        return i

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
