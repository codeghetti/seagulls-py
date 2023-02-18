from uuid import uuid4

from random import randint

from seagulls.cat_demos.app._mob_controls_component import MobControlsComponentId
from seagulls.cat_demos.app._sprites import MySprites
from seagulls.cat_demos.engine.v2.animation._animation_component import SpriteAnimationComponentId
from seagulls.cat_demos.engine.v2.components._identity import GameObjectId
from seagulls.cat_demos.engine.v2._position_component import PositionComponentId, Vector
from seagulls.cat_demos.engine.v2._scene import GameSceneObjects
from seagulls.cat_demos.engine.v2._sprite_component import SpriteComponentId
from seagulls.cat_demos.app._player_controls_component import PlayerControlsComponentId


class MainScene:

    _scene_client: GameSceneObjects

    def __init__(self, scene_objects: GameSceneObjects) -> None:
        self._scene_client = scene_objects

    def load_scene(self) -> None:
        self._spawn_player()
        # self._spawn_enemies()

    def tick(self) -> None:
        pass
        # if randint(0, 100) == 100:
        #     self._spawn_enemies()

    def _spawn_player(self) -> None:
        gobject = GameObjectId("player")
        self._scene_client.create_object(gobject)
        self._scene_client.attach_component(gobject, PositionComponentId)
        self._scene_client.attach_component(gobject, PlayerControlsComponentId)
        self._scene_client.attach_component(gobject, SpriteComponentId)
        self._scene_client.attach_component(gobject, SpriteAnimationComponentId)
        components = self._scene_client.get_object_components(gobject)
        components.get(SpriteComponentId).set_sprite(MySprites.PLAYER_IDLE_1)

        animation_component = components.get(SpriteAnimationComponentId)
        animation_component.set_animation(
            frames=[
                MySprites.PLAYER_IDLE_1,
                MySprites.PLAYER_IDLE_2,
            ],
            duration=1000,
            loop=True,
        )

    def _spawn_enemies(self) -> None:
        for x in range(5):
            uid = str(uuid4())
            gobject = GameObjectId(f"enemy.{uid}")
            position = Vector(x=randint(0, 1000), y=randint(0, 1000))
            self._scene_client.create_object(gobject)
            self._scene_client.attach_component(gobject, PositionComponentId)
            self._scene_client.attach_component(gobject, SpriteComponentId)
            self._scene_client.attach_component(gobject, MobControlsComponentId)
            components = self._scene_client.get_object_components(gobject)
            components.get(SpriteComponentId).set_sprite(MySprites.ENEMY_IDLE)
            components.get(PositionComponentId).update(position)
