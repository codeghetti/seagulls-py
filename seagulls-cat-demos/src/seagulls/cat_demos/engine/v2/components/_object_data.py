from abc import abstractmethod

from typing import Generic, NamedTuple, Protocol, TypeVar

T_DataType = TypeVar("T_DataType", bound=NamedTuple)


class ObjectDataId(NamedTuple, Generic[T_DataType]):
    name: str


class GameObjectData(NamedTuple, Generic[T_DataType]):
    data_id: ObjectDataId[T_DataType]
    data: T_DataType


class ObjectDataProvider(Protocol[T_DataType]):
    @abstractmethod
    def __call__(self) -> T_DataType:
        pass
