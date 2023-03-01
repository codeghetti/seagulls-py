from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import Optional, Tuple

from seagulls.cat_demos.engine.v2._scene import IProvideGameObjectComponent
from seagulls.cat_demos.engine.v2._sprite_component import GameSprite, SpriteComponent, SpriteComponentClient
from seagulls.cat_demos.engine.v2.components._game_components import GameComponentId
from seagulls.cat_demos.engine.v2.components._scene_objects import GameObjectId

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _AnimationConfig:
    started_at: datetime
    frames: Tuple[GameSprite, ...]
    duration: int
    loop: bool


class SpriteAnimationComponent:

    _game_object: GameObjectId
    _sprite_component: SpriteComponent
    _current_animation: Optional[_AnimationConfig]

    def __init__(self, game_object: GameObjectId, sprite_component: SpriteComponent) -> None:
        self._game_object = game_object
        self._sprite_component = sprite_component
        self._current_animation = None

    def tick(self) -> None:
        config = self._current_animation
        if config is None:
            return

        now = datetime.now()
        time_elapsed = (now - config.started_at).total_seconds() * 1000.0  # 3120
        if not config.loop and time_elapsed > config.duration:
            return

        self._sprite_component.set_sprite(self._get_sprite(config, time_elapsed))

    def _get_sprite(self, config, time_elapsed) -> GameSprite:
        remainder = time_elapsed % config.duration  # 1120
        num_frames = len(config.frames)  # 2
        ms_per_frame = config.duration / num_frames  # 1000
        logger.debug(f"remainder: {remainder}")
        logger.debug(f"num_frames: {num_frames}")
        logger.debug(f"ms_per_frame: {ms_per_frame}")
        for x in range(num_frames):
            ms_limit = (x + 1) * ms_per_frame  # 1000
            logger.debug(f"ms_limit: {ms_limit}")
            if remainder <= ms_limit:
                return config.frames[x]

        raise RuntimeError("Couldn't find animation frame")

    def set_animation(self, frames: Tuple[GameSprite, ...], duration: int, loop: bool) -> None:
        self._current_animation = _AnimationConfig(
            started_at=datetime.now(),
            frames=frames,
            duration=duration,
            loop=loop,
        )


SpriteAnimationComponentId = GameComponentId[SpriteAnimationComponent]("sprite-animation")


class SpriteAnimationComponentClient(IProvideGameObjectComponent[SpriteAnimationComponent]):

    _sprite_component_client: SpriteComponentClient

    def __init__(self, sprite_component_client: SpriteComponentClient) -> None:
        self._sprite_component_client = sprite_component_client

    def tick(self, game_object: GameObjectId) -> None:
        self.get(game_object).tick()

    @lru_cache()
    def get(self, game_object: GameObjectId) -> SpriteAnimationComponent:
        logger.debug(f"attaching animation component to game object: {game_object}")
        return SpriteAnimationComponent(
            game_object=game_object,
            sprite_component=self._sprite_component_client.get(game_object),
        )
