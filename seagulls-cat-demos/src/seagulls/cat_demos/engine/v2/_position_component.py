from __future__ import annotations

from functools import lru_cache

from typing import TypeAlias

from seagulls.cat_demos.engine.v2.components._identity import EntityType, GameComponentId, \
    GameObjectId
from ._point import Point
from ._scene import IProvideGameObjectComponent

Position: TypeAlias = Point
Vector: TypeAlias = Point


class PositionComponent:

    _object: GameObjectId
    _position: Position

    def __init__(self, game_object: GameObjectId) -> None:
        self._object = game_object
        self._position = Position.zero()

    def get(self) -> Position:
        return self._position

    def update(self, position: Position) -> None:
        self._position = position


PositionComponentId = GameComponentId[PositionComponent]("position")


class PositionComponentClient(IProvideGameObjectComponent[PositionComponent]):

    def tick(self, game_object: GameObjectId) -> None:
        pass

    @lru_cache()
    def get(self, game_object: GameObjectId) -> EntityType:
        return PositionComponent(game_object=game_object)
