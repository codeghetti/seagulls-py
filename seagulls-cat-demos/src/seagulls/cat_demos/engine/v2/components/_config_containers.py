from abc import abstractmethod
from typing import Any, Dict, NamedTuple, Protocol, Tuple, TypeAlias, TypeVar

from ._entities import TypedEntityId

T_GameConfigType = TypeVar("T_GameConfigType", bound=NamedTuple)
Tco_GameConfigType = TypeVar("Tco_GameConfigType", bound=NamedTuple, covariant=True)
GameConfigId: TypeAlias = TypedEntityId[Tco_GameConfigType]


class GameConfigProvider(Protocol[Tco_GameConfigType]):
    @abstractmethod
    def __call__(self) -> Tco_GameConfigType:
        pass


class GameConfigContainer(Protocol):
    @abstractmethod
    def get(self, config_id: GameConfigId[Tco_GameConfigType]) -> Tco_GameConfigType:
        pass


class GameConfigFactory(GameConfigContainer):
    _providers: Dict[GameConfigId[Any], GameConfigProvider[Any]]

    @staticmethod
    def with_providers(
        *provider: Tuple[
            GameConfigId[Tco_GameConfigType], GameConfigProvider[Tco_GameConfigType]
        ],
    ) -> "GameConfigFactory":
        i = GameConfigFactory()
        for p in provider:
            i.set(p[0], p[1])
        return i

    def __init__(self) -> None:
        self._providers = {}

    def set_missing(
        self,
        *provider: Tuple[
            GameConfigId[Tco_GameConfigType], GameConfigProvider[Tco_GameConfigType]
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
        config_id: GameConfigId[Tco_GameConfigType],
        provider: GameConfigProvider[Tco_GameConfigType],
    ) -> None:
        if config_id in self._providers:
            raise RuntimeError(f"duplicate entity found: {config_id}")

        self._providers[config_id] = provider

    def get(self, config_id: GameConfigId[Tco_GameConfigType]) -> Tco_GameConfigType:
        if config_id not in self._providers:
            raise RuntimeError(f"entity not found: {config_id}")

        return self._providers[config_id]()
