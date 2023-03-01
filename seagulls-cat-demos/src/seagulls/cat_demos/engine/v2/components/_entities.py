from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeAlias, TypeVar

EntityType = TypeVar("EntityType")


@dataclass(frozen=True)
class EntityId:
    """
    Identity object used as a primary key in various collections.

    This class is often used as an alternative to simple strings when trying to identify a unique
    entry in a collection. For example, we can use them to identify the game objects present in the
    current scene.

    Example:
        Get the player object from the scene::
            things.get(EntityId("player"))
    """
    name: str

    @classmethod
    def make(cls, name: str) -> EntityId:
        return cls(f"{cls.__module__}/{cls.__name__}/{name}")

    def __post_init__(self) -> None:
        pass


class TypedEntityId(EntityId, Generic[EntityType]):
    """
    Typed identity object used as a primary key in various collections.

    Unlike the EntityId object, this class has an attached type that can be used when we want to
    allow collections to hold a mixture of types. For example, we could use this to retrieve a
    component of a certain type from a game object.

    Example:
        Get the player's position component::
            player.get_component(TypedEntityId[PositionComponent]("position"))
        You can use a TypeAlias as a shortcut to create a simpler API for users::
            GameComponentId: TypeAlias = TypedEntityId
            PositionComponentId: TypeAlias = GameComponentId[PositionComponent]
            class SeagullComponents:
                POSITION = PositionComponentId("position")
        With a handful of aliases, our users can get an intuitive API with proper types::
            player.get_component(SeagullComponents.POSITION)
    """


GameSceneId: TypeAlias = EntityId
