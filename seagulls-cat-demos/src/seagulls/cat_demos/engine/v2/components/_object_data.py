from typing import Generic, NamedTuple, TypeVar

T_DataType = TypeVar("T_DataType", bound=NamedTuple)


class ObjectDataId(NamedTuple, Generic[T_DataType]):
    name: str


class GameObjectData(NamedTuple, Generic[T_DataType]):
    data_id: ObjectDataId[T_DataType]
    data: T_DataType
