from dataclasses import dataclass
from typing import Set, NamedTuple, Dict


@dataclass(frozen=True)
class GameObject:
    key: str


class GameObjectClient:

    _objects: Set[GameObject]

    def __init__(self) -> None:
        self._objects = set()

    def execute(self) -> None:
        pass

    def add(self, item: GameObject) -> None:
        self._objects.add(item)

    def get(self, key: str) -> GameObject:
        for item in self._objects:
            if item.key == key:
                return item

        raise RuntimeError(f"GameObject not found: {key}")


class GameObjectComponentsClient:
    pass


class Position(NamedTuple):
    x: int
    y: int


class GameObjectPositionClient:

    _positions: Dict[GameObject, Position]

    def __init__(self) -> None:
        self._positions = {}

    def set_position(self, game_object: GameObject, position: Position) -> None:
        self._positions[game_object] = position

    def get_position(self, game_object: GameObject) -> Position:
        return self._positions[game_object]


class Size(NamedTuple):
    height: int
    width: int


class PositionComponent:

    _position: Position

    def __init__(self, position: Position) -> None:
        self._position = position

    def get_position(self) -> Position:
        return self._position

    def update_position(self, position: Position) -> None:
        self._position = position


class RigidbodyComponent:

    _position_component: PositionComponent

    def __init__(self, position_component: PositionComponent) -> None:
        self._position_component = position_component

    def tick(self) -> None:
        pass
