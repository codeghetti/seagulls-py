from __future__ import annotations

import logging
from abc import abstractmethod
from functools import lru_cache
from typing import Generic, NamedTuple, Protocol

from pygame.constants import SRCALPHA
from pygame.image import load
from pygame.surface import Surface

from seagulls.cat_demos.engine.v2.components._identity import EntityId, EntityType
from seagulls.cat_demos.engine.v2.components._object_components import GameComponentId
from seagulls.cat_demos.engine.v2.components._scene_objects import GameObjectId
from seagulls.cat_demos.engine.v2.position._position_component import Position, PositionComponent, \
    PositionComponentClient
from seagulls.cat_demos.engine.v2.window._window import WindowClient
from ._resources import ResourceClient
from ._scene import IProvideGameObjectComponent
from ._size import Size

logger = logging.getLogger(__name__)


class GameSprite(EntityId, Generic[EntityType]):
    @classmethod
    def none(cls) -> GameSprite:
        return cls("__none__")


class _SpriteConfig(NamedTuple):
    resource: str
    position: Position
    size: Size


class IManageSprites(Protocol):

    @abstractmethod
    def register_sprite(
            self,
            sprite: GameSprite,
            resource: str,
            position: Position,
            size: Size,
    ) -> None:
        pass

    @abstractmethod
    def get_sprite(self, sprite: GameSprite) -> Surface:
        pass


class SpriteComponent:
    _sprite_manager: IManageSprites
    _window_client: WindowClient
    _position_component: PositionComponent
    _game_object: GameObjectId
    _sprite: GameSprite

    def __init__(
        self,
        sprite_manager: IManageSprites,
        window_client: WindowClient,
        position_component: PositionComponent,
        game_object: GameObjectId,
    ) -> None:
        self._sprite_manager = sprite_manager
        self._window_client = window_client
        self._position_component = position_component
        self._game_object = game_object
        self._sprite = GameSprite("enemy.idle")

    def set_sprite(self, sprite: GameSprite) -> None:
        self._sprite = sprite

    def tick(self) -> None:
        position = self._position_component.get()
        sprite = self._sprite
        game_object = self._game_object

        logger.debug(
            f"rendering sprite {sprite} for game object {game_object} at position {position}")

        self._window_client.get_surface().blit(
            self._sprite_manager.get_sprite(sprite),
            (position.x, position.y),
        )


SpriteComponentId = GameComponentId[SpriteComponent]("sprite")


class SpriteComponentClient(IProvideGameObjectComponent[SpriteComponent], IManageSprites):

    _window_client: WindowClient
    _resources_client: ResourceClient
    _position_client: PositionComponentClient

    def __init__(
        self,
        window_client: WindowClient,
        resources_client: ResourceClient,
        position_client: PositionComponentClient,
    ) -> None:
        self._window_client = window_client
        self._resources_client = resources_client
        self._position_client = position_client
        self._sprites = {}
        self._object_sprites = {}

    def tick(self, game_object: GameObjectId) -> None:
        self.get(game_object).tick()

    @lru_cache()
    def get(self, game_object: GameObjectId) -> SpriteComponent:
        return SpriteComponent(
            sprite_manager=self,
            window_client=self._window_client,
            position_component=self._position_client.get(game_object),
            game_object=game_object,
        )

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

    def get_sprite(self, sprite: GameSprite) -> Surface:
        config = self._sprites[sprite]
        path = self._resources_client.get_path(config.resource)
        logger.debug(f"sprite resource found: {path}")
        sheet = load(path).convert_alpha()
        unit = Surface((config.size.width, config.size.height), SRCALPHA, 32)
        unit.blit(
            sheet,
            (0, 0),
            (config.position.x, config.position.y, config.size.width, config.size.height),
        )
        return unit

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
