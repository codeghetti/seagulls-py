from typing import TypeVar, Dict, Type, Any

ObjectType = TypeVar("ObjectType")


class DiContainerRepository:
    _containers: Dict[Any, Any]

    def __init__(self):
        self._containers = {}

    def register(self, key: Type[ObjectType], container: ObjectType) -> None:
        self._containers[key] = container

    def get(self, key: Type[ObjectType]) -> ObjectType:
        if key not in self._containers:
            raise DiContainerNotFoundError(key)

        return self._containers[key]


class DiContainerNotFoundError(Exception):

    _key: Any

    def __init__(self, key: Type[ObjectType]):
        super().__init__(f"DI Container Not Found: {key}")
        self._key = key
