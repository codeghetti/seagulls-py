from dataclasses import dataclass

from abc import abstractmethod

from pygame import Surface
from typing import Protocol, Tuple

from seagulls.cat_demos._object_position import Position


@dataclass(frozen=True)
class GameObject:
    key: str


class IProvideSurfaces(Protocol):
    """
    Interface for class that provides the Surface of a single item.
    """

    @abstractmethod
    def get_surface(self) -> Surface:
        pass


class IProvidePositions(Protocol):
    """
    Interface for class that provides the Position of a single item.
    """

    @abstractmethod
    def get_position(self) -> Position:
        pass


class IProvideGameObjects(Protocol):

    @abstractmethod
    def get_game_objects(self) -> Tuple[GameObject, ...]:
        pass


class IProvideObjectSprites(Protocol):
    """
    Maps a GameObject to its sprite Surface.
    """

    @abstractmethod
    def get_sprite(self, game_object: GameObject) -> Surface:
        pass


class IProvideObjectPositions(Protocol):
    """
    Maps a GameObject to its Position.
    """

    @abstractmethod
    def get_position(self, game_object: GameObject) -> Position:
        pass


class RenderSceneObjects:

    def __init__(
        self,
        surface_client: IProvideSurfaces,
        game_objects_client: IProvideGameObjects,
        object_sprites_client: IProvideObjectSprites,
        object_positions_client: IProvideObjectPositions,
    ) -> None:
        self._surface_client = surface_client
        self._game_objects_client = game_objects_client
        self._object_sprites_client = object_sprites_client
        self._object_positions_client = object_positions_client

    def execute(self) -> None:
        surface = self._surface_client.get_surface()
        for game_object in self._game_objects_client.get_game_objects():
            sprite = self._object_sprites_client.get_sprite(game_object)
            surface.blit(sprite, self._object_positions_client.get_position(game_object))
