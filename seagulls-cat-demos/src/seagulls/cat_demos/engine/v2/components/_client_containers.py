from abc import abstractmethod
from functools import lru_cache
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    Protocol,
    Tuple,
    TypeVar
)

from ._entities import GameClientId
from ._object_data import ObjectDataProvider

Tco_GameClientType = TypeVar("Tco_GameClientType", covariant=True)
T_GameClientType = TypeVar("T_GameClientType")


class GameClientProvider(Protocol[Tco_GameClientType]):
    @abstractmethod
    def __call__(self) -> Tco_GameClientType:
        pass


class GameClientContainer(Protocol):
    @abstractmethod
    def get(
        self, client_id: GameClientId[Tco_GameClientType]
    ) -> Tco_GameClientType:
        pass


class TypedGameClientContainer(Protocol[T_GameClientType]):
    """
    A container object that provides components of a single type.
    """

    _container: GameClientContainer

    def __init__(self, container: GameClientContainer) -> None:
        self._container = container

    def get(self, client_name: str) -> T_GameClientType:
        return self._container.get(self.client_id(client_name))

    def client_id(self, client_name: str) -> GameClientId[T_GameClientType]:
        return GameClientId[T_GameClientType](client_name)


class GameClientFactory(GameClientContainer):

    _providers: Dict[GameClientId[Any], GameClientProvider[Any]]

    @staticmethod
    def with_providers(
        *provider: Tuple[
            GameClientId[Tco_GameClientType], GameClientProvider[Tco_GameClientType]
        ],
    ) -> "GameClientFactory":
        i = GameClientFactory()
        for p in provider:
            i.set(p[0], p[1])
        return i

    def __init__(self) -> None:
        self._providers = {}

    def set_missing(
        self,
        *provider: Tuple[
            GameClientId[Tco_GameClientType], GameClientProvider[Tco_GameClientType]
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
        client_id: GameClientId[Tco_GameClientType],
        provider: GameClientProvider[Tco_GameClientType],
    ) -> None:
        if client_id in self._providers:
            raise RuntimeError(f"duplicate entity found: {client_id}")

        self._providers[client_id] = provider

    def get(
        self, client_id: GameClientId[Tco_GameClientType]
    ) -> Tco_GameClientType:
        if client_id not in self._providers:
            raise RuntimeError(f"entity not found: {client_id}")

        return self._providers[client_id]()


class CachedGameClientContainer(GameClientContainer):
    _container: GameClientContainer

    def __init__(self, container: GameClientContainer) -> None:
        self._container = container

    @lru_cache()
    def get(
        self, client_id: GameClientId[Tco_GameClientType]
    ) -> Tco_GameClientType:
        return self._container.get(client_id)


class ContextualGameClientContainer(GameClientContainer, Generic[T_GameClientType]):
    _container: GameClientContainer
    _context: ObjectDataProvider[Any]

    def __init__(
        self,
        container: GameClientContainer,
        context: ObjectDataProvider[Any],
    ) -> None:
        self._container = container
        self._context = context

    def get(
        self, client_id: GameClientId[Tco_GameClientType]
    ) -> Tco_GameClientType:
        # The public function is never cached because we want to add the context
        return self._get(client_id, self._context())

    @lru_cache()
    def _get(
        self, component_id: GameClientId[Tco_GameClientType], context: T_GameClientType
    ) -> Tco_GameClientType:
        # We don't have to use the context, we just want it in the args for caching
        return self._container.get(component_id)


class FilteredGameComponentRegistry(GameClientContainer):
    _container: GameClientContainer
    _context: GameClientProvider[Iterable[GameClientId]]

    def __init__(
        self,
        container: GameClientContainer,
        context: GameClientProvider[Iterable[GameClientId]],
    ) -> None:
        self._container = container
        self._context = context

    def get(
        self, client_id: GameClientId[Tco_GameClientType]
    ) -> Tco_GameClientType:
        if client_id not in self._context():
            raise RuntimeError(f"entity not found: {client_id}")

        return self._container.get(client_id)
