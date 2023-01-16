from typing import Generic, TypeVar

from dataclasses import dataclass


ComponentType = TypeVar("ComponentType")


@dataclass(frozen=True)
class _IdentityObject:
    name: str

    @classmethod
    def make(cls, name: str) -> "_IdentityObject":
        return cls(f"{cls.__module__}[{cls.__name__}][{name}]")


class GameObject(_IdentityObject):
    pass


class GameComponent(_IdentityObject, Generic[ComponentType]):
    pass
