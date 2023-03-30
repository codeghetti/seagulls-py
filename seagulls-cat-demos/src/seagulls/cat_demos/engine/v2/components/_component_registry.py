from abc import abstractmethod
from functools import lru_cache
from typing import Any, Dict, Generic, Protocol, Tuple, TypeVar

from seagulls.cat_demos.engine.v2._service_provider import ServiceProvider
from seagulls.cat_demos.engine.v2.components._entities import TypedEntityId

GameComponentType = TypeVar("GameComponentType")


class GameComponentId(TypedEntityId[GameComponentType]):
    pass


class GameComponentProvider(Protocol[GameComponentType]):

    @abstractmethod
    def __call__(self) -> GameComponentType:
        pass


class GameComponentFactory:

    _providers: Dict[GameComponentId[Any], GameComponentProvider[Any]]

    @staticmethod
    def with_providers(
            *provider: Tuple[GameComponentId[GameComponentType], GameComponentProvider[GameComponentType]],
    ) -> "GameComponentFactory":
        i = GameComponentFactory()
        for p in provider:
            i.set(p[0], p[1])
        return i

    def __init__(self) -> None:
        self._providers = {}

    def set_defaults(
        self,
        *provider: Tuple[GameComponentId[GameComponentType], GameComponentProvider[GameComponentType]],
    ) -> None:
        for p in provider:
            if p[0] not in self._providers:
                self.set(p[0], p[1])

    def set(
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


class GameComponentRegistry:

    _factory: GameComponentFactory

    def __init__(self, factory: GameComponentFactory) -> None:
        self._factory = factory

    @lru_cache()
    def get(self, entity_id: GameComponentId[GameComponentType]) -> GameComponentType:
        return self._factory.get(entity_id)


T = TypeVar("T")


class ContextualGameComponentRegistry(Generic[T]):

    _factory: GameComponentFactory
    _context_provider: ServiceProvider[T]

    def __init__(self, factory: GameComponentFactory, context_provider: ServiceProvider[T]) -> None:
        self._factory = factory
        self._context_provider = context_provider

    def get(self, entity_id: GameComponentId[GameComponentType]) -> GameComponentType:
        # The public function is never cached because we want to add the context
        return self._get(entity_id, self._context_provider())

    @lru_cache()
    def _get(self, entity_id: GameComponentId[GameComponentType], context: T) -> GameComponentType:
        # We don't have to use the context, we just want it in the args for caching
        return self._factory.get(entity_id)
