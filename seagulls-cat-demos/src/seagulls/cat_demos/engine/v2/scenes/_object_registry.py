from typing import Set, Tuple

from seagulls.cat_demos.engine.v2.components._identity import GameObjectId


class GameObjectRegistry:

    _objects: Set[GameObjectId]

    def __init__(self) -> None:
        self._objects = set()

    def add(self, game_object: GameObjectId) -> None:
        if game_object in self._objects:
            raise RuntimeError(f"Duplicate game object found: {game_object}")

        self._objects.add(game_object)

    def remove(self, game_object: GameObjectId) -> None:
        if game_object not in self._objects:
            raise RuntimeError(f"Game object not found: {game_object}")

    def find(self, game_object: GameObjectId) -> None:
        """
        If this method exists then it might return a standard game object component client.
        """
        if game_object not in self._objects:
            raise RuntimeError(f"Game object not found: {game_object}")

        raise NotImplementedError()

    def get_all(self) -> Tuple[GameObjectId, ...]:
        return tuple(self._objects)
