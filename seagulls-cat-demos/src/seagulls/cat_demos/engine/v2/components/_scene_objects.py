from typing import Set, Tuple

from ._game_objects import GameObjectId, IManageGameObjects


class SceneObjects(IManageGameObjects):

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
