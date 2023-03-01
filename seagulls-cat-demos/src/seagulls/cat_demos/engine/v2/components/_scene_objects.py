from typing import Set, Tuple, TypeAlias

from ._identity import EntityId

GameObjectId: TypeAlias = EntityId


class SceneObjects:

    _entities: Set[GameObjectId]

    def __init__(self) -> None:
        self._entities = set()

    def add(self, entity_id: GameObjectId) -> None:
        if entity_id in self._entities:
            raise RuntimeError(f"duplicate entity found: {entity_id}")

        self._entities.add(entity_id)

    def remove(self, entity_id: GameObjectId) -> None:
        if entity_id not in self._entities:
            raise RuntimeError(f"entity not found: {entity_id}")

        self._entities.remove(entity_id)

    def clear(self) -> None:
        self._entities.clear()

    def get(self) -> Tuple[GameObjectId, ...]:
        return tuple(self._entities)
