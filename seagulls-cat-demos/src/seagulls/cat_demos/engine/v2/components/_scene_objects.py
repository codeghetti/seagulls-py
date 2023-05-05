import logging
from typing import Any, Dict, Set, Tuple, TypeVar

from ._entities import GameObjectId
from ._object_data import GameObjectData, ObjectDataId

logger = logging.getLogger(__name__)
T = TypeVar("T")


class SceneObjects:
    _entities: Dict[GameObjectId, Set[ObjectDataId]]
    _data: Dict[ObjectDataId[Any], Dict[GameObjectId, GameObjectData[Any]]]

    def __init__(self) -> None:
        self._entities = {}
        self._data = {}

    def add(self, object_id: GameObjectId) -> None:
        if object_id in self._entities:
            raise RuntimeError(f"duplicate entity found: {object_id}")

        self._entities[object_id] = set()

    def remove(self, object_id: GameObjectId) -> None:
        if object_id not in self._entities:
            raise RuntimeError(f"entity not found: {object_id}")

        del self._entities[object_id]

    def get(self) -> Tuple[GameObjectId, ...]:
        return tuple(self._entities.keys())

    def set_data(
        self,
        object_id: GameObjectId,
        data_id: ObjectDataId[T],
        config: T,
    ) -> None:
        if data_id not in self._data:
            self._data[data_id] = {}

        self._entities[object_id].add(data_id)
        self._data[data_id][object_id] = config

    def get_data(
        self,
        object_id: GameObjectId,
        data_id: ObjectDataId[T],
    ) -> T:
        return self._data[data_id][object_id]

    def find_by_data_id(
        self, data_id: ObjectDataId
    ) -> Tuple[GameObjectId, ...]:
        result = []
        for e, cs in self._entities.items():
            if data_id in cs:
                result.append(e)

        return tuple(result)
