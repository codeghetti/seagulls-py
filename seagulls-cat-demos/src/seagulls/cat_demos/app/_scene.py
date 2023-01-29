from seagulls.cat_demos.engine.v2._entities import GameObject
from seagulls.cat_demos.engine.v2._position_component import PositionComponentId
from seagulls.cat_demos.engine.v2._scene import GameSceneObjects
from seagulls.cat_demos.engine.v2._sprite_component import SpriteComponentId
from seagulls.cat_demos.app.player_controls_component import PlayerControlsComponentId


class MainScene:

    _scene_objects: GameSceneObjects

    def __init__(self, scene_objects: GameSceneObjects) -> None:
        self._scene_objects = scene_objects

    def load_scene(self) -> None:
        self._spawn_player()

        self._scene_objects.create_object(GameObject("enemy.1"))

        # self._scene_objects.attach_component(
        #     GameObject("enemy.1"),
        #     GameComponent[MobControlsComponent]("mob-controls"))

        # self._scene_objects.attach_component(
        #     GameObject("enemy.2"),
        #     GameComponent[MobControlsComponent]("mob-controls"))

        # self._sprites.attach_sprite(GameObject("enemy.1"), GameSprite("enemy.idle"))

    def _spawn_player(self) -> None:
        self._scene_objects.create_object(GameObject("player"))
        self._scene_objects.attach_component(GameObject("player"), PositionComponentId)
        self._scene_objects.attach_component(GameObject("player"), PlayerControlsComponentId)
        self._scene_objects.attach_component(GameObject("player"), SpriteComponentId)

    def tick(self) -> None:
        pass
