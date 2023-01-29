from uuid import uuid4

from random import randint

from seagulls.cat_demos.app.mob_controls_component import MobControlsComponentId
from seagulls.cat_demos.engine.v2._entities import GameObject
from seagulls.cat_demos.engine.v2._position_component import PositionComponentId, Vector
from seagulls.cat_demos.engine.v2._scene import GameSceneObjects
from seagulls.cat_demos.engine.v2._sprite_component import GameSprite, SpriteComponentId
from seagulls.cat_demos.app.player_controls_component import PlayerControlsComponentId


class MainScene:

    _scene_objects: GameSceneObjects

    def __init__(self, scene_objects: GameSceneObjects) -> None:
        self._scene_objects = scene_objects

    def load_scene(self) -> None:
        self._spawn_player()
        self._spawn_enemies()

    def tick(self) -> None:
        if randint(0, 100) == 100:
            self._spawn_enemies()

    def _spawn_player(self) -> None:
        gobject = GameObject("player")
        self._scene_objects.create_object(gobject)
        self._scene_objects.attach_component(gobject, PositionComponentId)
        self._scene_objects.attach_component(gobject, PlayerControlsComponentId)
        self._scene_objects.attach_component(gobject, SpriteComponentId)
        components = self._scene_objects.get_object_components(gobject)
        components.get(SpriteComponentId).set_sprite(GameSprite("player.idle"))

    def _spawn_enemies(self) -> None:
        for x in range(5):
            uid = str(uuid4())
            gobject = GameObject(f"enemy.{uid}")
            position = Vector(x=randint(0, 1000), y=randint(0, 1000))
            self._scene_objects.create_object(gobject)
            self._scene_objects.attach_component(gobject, PositionComponentId)
            self._scene_objects.attach_component(gobject, SpriteComponentId)
            self._scene_objects.attach_component(gobject, MobControlsComponentId)
            components = self._scene_objects.get_object_components(gobject)
            components.get(SpriteComponentId).set_sprite(GameSprite("enemy.idle"))
            components.get(PositionComponentId).update(position)
