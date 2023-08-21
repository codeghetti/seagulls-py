import logging
from typing import Any, Dict, FrozenSet, Set, Tuple, TypeVar

from ._entities import GameObjectId, GameSceneId
from ._object_data import GameObjectData, ObjectDataId
from ..scenes._scene_client import SceneContext

logger = logging.getLogger(__name__)
T = TypeVar("T")


class SceneObjects:
    _entities: Dict[Tuple[GameSceneId, GameObjectId], Set[ObjectDataId]]
    _data: Dict[Tuple[GameSceneId, ObjectDataId[Any]], Dict[GameObjectId, GameObjectData[Any]]]
    _scene_context: SceneContext

    def __init__(self, scene_context: SceneContext) -> None:
        self._entities = {}
        self._data = {}
        self._scene_context = scene_context

    def add(self, object_id: GameObjectId) -> None:
        scene_id = self._scene_context.get()
        key = (scene_id, object_id)
        if key in self._entities:
            raise RuntimeError(f"duplicate entity found: {object_id}")

        self._entities[key] = set()

    def remove(self, object_id: GameObjectId) -> None:
        scene_id = self._scene_context.get()
        key = (scene_id, object_id)

        if key not in self._entities:
            raise RuntimeError(f"entity not found: {object_id}")

        del self._entities[key]

    def get(self) -> Tuple[GameObjectId, ...]:
        scene_id = self._scene_context.get()
        objs = [key[1] for key in self._entities.keys() if key[0] == scene_id]
        return tuple(objs)

    def set_data(
        self,
        object_id: GameObjectId,
        data_id: ObjectDataId[T],
        config: T,
    ) -> None:
        scene_id = self._scene_context.get()
        data_key = (scene_id, data_id)
        obj_key = (scene_id, object_id)

        if data_key not in self._data:
            self._data[data_key] = {}

        self._entities[obj_key].add(data_id)
        self._data[data_key][object_id] = config

    def get_data(
        self,
        object_id: GameObjectId,
        data_id: ObjectDataId[T],
    ) -> T:
        scene_id = self._scene_context.get()
        key = (scene_id, data_id)
        return self._data[key][object_id]

    def find_by_data_id(self, data_id: ObjectDataId) -> FrozenSet[GameObjectId]:
        scene_id = self._scene_context.get()
        result = set()
        for entity_key, entity_data in self._entities.items():
            if scene_id == entity_key[0] and data_id in entity_data:
                result.add(entity_key[1])

        return frozenset(result)
