from abc import abstractmethod
from typing import Any, Dict, NamedTuple, Protocol, Tuple, TypeVar

from ._entities import TypedEntityId

GameConfigType = TypeVar("GameConfigType", bound=NamedTuple)


class GameConfigId(TypedEntityId[GameConfigType]):
    pass


class GameConfigProvider(Protocol[GameConfigType]):

    @abstractmethod
    def __call__(self) -> GameConfigType:
        pass


class GameConfigContainer(Protocol):

    @abstractmethod
    def get(self, config_id: GameConfigId[GameConfigType]) -> GameConfigType:
        pass


class GameConfigFactory(GameConfigContainer):

    _providers: Dict[GameConfigId[Any], GameConfigProvider[Any]]

    @staticmethod
    def with_providers(
            *provider: Tuple[GameConfigId[GameConfigType], GameConfigProvider[GameConfigType]],
    ) -> "GameConfigFactory":
        i = GameConfigFactory()
        for p in provider:
            i.set(p[0], p[1])
        return i

    def __init__(self) -> None:
        self._providers = {}

    def set_missing(
        self,
        *provider: Tuple[GameConfigId[GameConfigType], GameConfigProvider[GameConfigType]],
    ) -> None:
        """
        Merge the providers into the current instance, ignoring any duplicates.
        """
        for p in provider:
            if p[0] not in self._providers:
                self.set(p[0], p[1])

    def set(
        self,
        config_id: GameConfigId[GameConfigType],
        provider: GameConfigProvider[GameConfigType],
    ) -> None:
        if config_id in self._providers:
            raise RuntimeError(f"duplicate entity found: {config_id}")

        self._providers[config_id] = provider

    def get(self, config_id: GameConfigId[GameConfigType]) -> GameConfigType:
        if config_id not in self._providers:
            raise RuntimeError(f"entity not found: {config_id}")

        return self._providers[config_id]()
