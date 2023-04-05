from abc import abstractmethod
from typing import Iterable, Protocol, TypeAlias

from ._entities import EntityId

GameObjectId: TypeAlias = EntityId


class IManageGameObjects(Protocol):
    @abstractmethod
    def add(self, entity_id: GameObjectId) -> None:
        pass

    @abstractmethod
    def remove(self, entity_id: GameObjectId) -> None:
        pass

    @abstractmethod
    def get(self) -> Iterable[GameObjectId]:
        pass
