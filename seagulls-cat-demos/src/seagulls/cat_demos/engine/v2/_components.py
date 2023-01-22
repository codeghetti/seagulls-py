from __future__ import annotations

import logging
from pygame.constants import SRCALPHA
from pygame.image import load
from pygame.surface import Surface

from typing import Dict, NamedTuple, Tuple, TypeAlias

from ._entities import GameObject, GameSprite
from ._resources import ResourceClient
from ._scene import ITick, IUpdate
from ._window import GameWindowClient

logger = logging.getLogger(__name__)


class Point(NamedTuple):
    x: float
    y: float

    def __add__(self, other: Tuple[float, float]) -> Point:
        return Point(x=self.x + other[0], y=self.y + other[1])

    def __sub__(self, other: Tuple[float, float]) -> Point:
        return Point(x=self.x - other[0], y=self.y - other[1])

    @classmethod
    def zero(cls) -> Point:
        return cls(0, 0)


Position: TypeAlias = Point
Direction: TypeAlias = Point


class Size(NamedTuple):
    height: float
    width: float

    def __add__(self, other: Tuple[float, float]) -> Size:
        return Size(height=self.height + other[0], width=self.width + other[1])

    def __sub__(self, other: Tuple[float, float]) -> Size:
        return Size(height=self.height - other[0], width=self.width - other[1])


class PositionComponent(ITick):
    _positions: Dict[GameObject: Position]

    def __init__(self) -> None:
        self._positions = {}

    def tick(self) -> None:
        logger.error("position component tick")

    def set_position(self, game_object: GameObject, position: Position) -> None:
        self._positions[game_object] = position

    def get_position(self, game_object: GameObject) -> Position:
        return self._positions.get(game_object, Position.zero())


class MobControlsComponent(ITick, IUpdate):

    _position_component: PositionComponent

    def __init__(self, position_component: PositionComponent) -> None:
        self._position_component = position_component

    def tick(self) -> None:
        logger.error("mob controls component tick")

    def update(self, game_object: GameObject) -> None:
        logger.error(f"mob controls component update: {game_object}")
        current = self._position_component.get_position(game_object)
        self._position_component.set_position(game_object, current + Position(1, 0))


class _SpriteConfig(NamedTuple):
    resource: str
    position: Position
    size: Size


class SpriteComponent(ITick):

    _window_client: GameWindowClient
    _resources_client: ResourceClient
    _position_component: PositionComponent
    _sprites: Dict[GameSprite, _SpriteConfig]
    _object_sprites: Dict[GameObject, GameSprite]

    def __init__(
        self,
        window_client: GameWindowClient,
        resources_client: ResourceClient,
        position_component: PositionComponent,
    ) -> None:
        self._window_client = window_client
        self._resources_client = resources_client
        self._position_component = position_component
        self._sprites = {}
        self._object_sprites = {}

    def tick(self) -> None:
        for game_object, sprite in self._object_sprites.items():
            position = self._position_component.get_position(game_object)
            logger.error(
                f"rendering sprite {sprite} for game object {game_object} at position {position}")
            config = self._sprites[sprite]
            path = self._resources_client.get_path(config.resource)
            logger.error(f"sprite resource found: {path}")
            sheet = load(path).convert_alpha()
            unit = Surface((config.size.width, config.size.height), SRCALPHA, 32)
            unit.blit(
                sheet,
                (0, 0),
                (config.position.x, config.position.y, config.size.width, config.size.height),
            )
            self._window_client.get_surface().blit(unit, (position.x, position.y))

    def register_sprite(
        self,
        sprite: GameSprite,
        resource: str,
        position: Position,
        size: Size,
    ) -> None:
        if sprite in self._sprites:
            raise RuntimeError(f"Duplicate sprite registered: {sprite}")
        self._sprites[sprite] = self._build_sprite_config(resource, position, size)

    def attach_sprite(self, game_object: GameObject, sprite: GameSprite) -> None:
        if sprite not in self._sprites:
            raise RuntimeError(f"Sprite not found: {sprite}")

        self._object_sprites[game_object] = sprite

    def _build_sprite_config(
        self,
        resource: str,
        position: Position,
        size: Size,
    ) -> _SpriteConfig:
        return _SpriteConfig(
            resource=resource,
            position=position,
            size=size,
        )
