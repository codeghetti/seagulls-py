from seagulls.cat_demos.engine.v2.components._identity import GameObjectId
from seagulls.cat_demos.engine.v2.scenes._object_registry import GameObjectRegistry


class OpenMainMenuScene:

    _game_objects: GameObjectRegistry

    def __init__(self, game_objects: GameObjectRegistry) -> None:
        self._game_objects = game_objects

    def execute(self) -> None:
        print("open scene")
        self._game_objects.add(GameObjectId("title"))
        self._game_objects.add(GameObjectId("game.a"))
        self._game_objects.add(GameObjectId("game.b"))
        self._game_objects.add(GameObjectId("game.c"))


class CloseMainMenuScene:

    _game_objects: GameObjectRegistry

    def execute(self) -> None:
        print("close scene")
