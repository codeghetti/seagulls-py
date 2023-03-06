from seagulls.cat_demos.engine.v2.components._scene_objects import GameObjectId, SceneObjects
from seagulls.cat_demos.engine.v2.position._position_component import PositionObjectComponentId


class OpenMainMenuScene:

    _scene_objects: SceneObjects

    def __init__(self, scene_objects: SceneObjects) -> None:
        self._scene_objects = scene_objects

    def execute(self) -> None:
        print("open scene")
        self._scene_objects.add(GameObjectId("title"))
        self._scene_objects.attach_component(GameObjectId("title"), PositionObjectComponentId)
        p = self._scene_objects.get_component(GameObjectId("title"), PositionObjectComponentId)
        print(f"title location: {p.get()}")

        self._scene_objects.add(GameObjectId("game.a"))
        self._scene_objects.add(GameObjectId("game.b"))
        self._scene_objects.add(GameObjectId("game.c"))


class CloseMainMenuScene:

    _scene_objects: SceneObjects

    def execute(self) -> None:
        print("close scene")
