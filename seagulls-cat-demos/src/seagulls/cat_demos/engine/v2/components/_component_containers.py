from abc import abstractmethod
from functools import lru_cache
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    Protocol,
    Tuple,
    TypeAlias,
    TypeVar
)

from ._entities import TypedEntityId
from ._service_provider import ServiceProvider

GameComponentType = TypeVar("GameComponentType", covariant=True)
T = TypeVar("T")
ObjectDataId: TypeAlias = TypedEntityId[GameComponentType]


class GameComponentProvider(Protocol[GameComponentType]):
    @abstractmethod
    def __call__(self) -> GameComponentType:
        pass


class GameComponentContainer(Protocol):
    @abstractmethod
    def get(
        self, component_id: ObjectDataId[GameComponentType]
    ) -> GameComponentType:
        pass


class TypedGameComponentContainer(Protocol[T]):
    """
    A container object that provides components of a single type.
    """

    @abstractmethod
    def get(self, component_id: ObjectDataId[T]) -> T:
        pass


class GameComponentFactory:
    _providers: Dict[ObjectDataId[Any], GameComponentProvider[Any]]

    @staticmethod
    def with_providers(
        *provider: Tuple[
            ObjectDataId[GameComponentType], GameComponentProvider[GameComponentType]
        ],
    ) -> "GameComponentFactory":
        i = GameComponentFactory()
        for p in provider:
            i.set(p[0], p[1])
        return i

    def __init__(self) -> None:
        self._providers = {}

    def set_missing(
        self,
        *provider: Tuple[
            ObjectDataId[GameComponentType], GameComponentProvider[GameComponentType]
        ],
    ) -> None:
        """
        Merge the providers into the current instance, ignoring any duplicates.
        """
        for p in provider:
            if p[0] not in self._providers:
                self.set(p[0], p[1])

    def set(
        self,
        component_id: ObjectDataId[GameComponentType],
        provider: GameComponentProvider[GameComponentType],
    ) -> None:
        if component_id in self._providers:
            raise RuntimeError(f"duplicate entity found: {component_id}")

        self._providers[component_id] = provider

    def get(
        self, component_id: ObjectDataId[GameComponentType]
    ) -> GameComponentType:
        if component_id not in self._providers:
            raise RuntimeError(f"entity not found: {component_id}")

        return self._providers[component_id]()


class CachedGameComponentContainer(GameComponentContainer):
    _factory: GameComponentContainer

    def __init__(self, factory: GameComponentContainer) -> None:
        self._factory = factory

    @lru_cache()
    def get(
        self, component_id: ObjectDataId[GameComponentType]
    ) -> GameComponentType:
        return self._factory.get(component_id)


class ContextualGameComponentContainer(GameComponentContainer, Generic[T]):
    _container: GameComponentContainer
    _context: ServiceProvider[T]

    def __init__(
        self, container: GameComponentContainer, context: ServiceProvider[T]
    ) -> None:
        self._container = container
        self._context = context

    def get(
        self, component_id: ObjectDataId[GameComponentType]
    ) -> GameComponentType:
        # The public function is never cached because we want to add the context
        return self._get(component_id, self._context())

    @lru_cache()
    def _get(
        self, component_id: ObjectDataId[GameComponentType], context: T
    ) -> GameComponentType:
        # We don't have to use the context, we just want it in the args for caching
        return self._container.get(component_id)


class FilteredGameComponentRegistry(GameComponentContainer):
    _container: GameComponentContainer
    _context: ServiceProvider[Iterable[ObjectDataId]]

    def __init__(
        self,
        container: GameComponentContainer,
        context: ServiceProvider[Iterable[ObjectDataId]],
    ) -> None:
        self._container = container
        self._context = context

    def get(
        self, component_id: ObjectDataId[GameComponentType]
    ) -> GameComponentType:
        if component_id not in self._context():
            raise RuntimeError(f"entity not found: {component_id}")

        return self._container.get(component_id)
