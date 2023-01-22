from seagulls.cat_demos.engine.v2._components import MobControlsComponent, SpriteComponent
from seagulls.cat_demos.engine.v2._entities import GameComponent, GameObject, GameSprite
from seagulls.cat_demos.engine.v2._scene import GameSceneObjects


class MainScene:

    _scene_objects: GameSceneObjects
    _sprites: SpriteComponent

    def __init__(self, scene_objects: GameSceneObjects, sprites: SpriteComponent) -> None:
        self._scene_objects = scene_objects
        self._sprites = sprites

    def load_scene(self) -> None:
        self._scene_objects.create_object(GameObject("player"))
        self._scene_objects.create_object(GameObject("enemy.1"))
        self._scene_objects.create_object(GameObject("enemy.2"))

        self._scene_objects.attach_component(
            GameObject("enemy.1"),
            GameComponent[MobControlsComponent]("mob-controls"))

        self._scene_objects.attach_component(
            GameObject("enemy.2"),
            GameComponent[MobControlsComponent]("mob-controls"))

        self._sprites.attach_sprite(GameObject("enemy.1"), GameSprite("enemy.idle"))

    def tick(self) -> None:
        pass
