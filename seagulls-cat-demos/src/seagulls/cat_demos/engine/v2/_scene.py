from abc import abstractmethod

from typing import Any, Dict, Protocol, Set, Tuple

from ._entities import ComponentType, GameComponent, GameObject


class ITick(Protocol):

    @abstractmethod
    def tick(self) -> None:
        pass


class GameScene(ITick):

    _objects: Set[GameObject]
    _components: Dict[GameComponent[Any], ITick]
    _component_objects: Dict[GameComponent, Set[GameObject]]

    def create_object(self, game_object: GameObject) -> None:
        if game_object in self._objects:
            raise RuntimeError(f"Duplicate object found: {game_object}")

        self._objects.add(game_object)

    def create_component(
        self,
        game_component: GameComponent[ComponentType],
        handler: ComponentType
    ) -> None:
        if game_component in self._components:
            raise RuntimeError(f"Duplicate component found: {game_component}")

        self._components[game_component] = handler
        self._component_objects[game_component] = set()

    def attach_component(self, game_object: GameObject, game_component: GameComponent[Any]) -> None:
        if game_object not in self._objects:
            raise RuntimeError(f"Object not found: {game_object}")

        if game_component not in self._components:
            raise RuntimeError(f"Component not found: {game_component}")

        if game_object in self._component_objects[game_component]:
            raise RuntimeError(f"Component already attached: {game_component}")

        self._component_objects[game_component].add(game_object)

    def tick(self) -> None:
        for component, handler in self._components.items():
            handler.tick()

    def get_object_component(
        self,
        game_object: GameObject,
        game_component: GameComponent[ComponentType],
    ) -> ComponentType:
        if game_object not in self._objects:
            raise RuntimeError(f"Object not found: {game_object}")

        if game_component not in self._components:
            raise RuntimeError(f"Component not found: {game_component}")

        if game_object not in self._component_objects[game_component]:
            raise RuntimeError(f"Component not attached to object: {game_component}, {game_object}")

        return self._components[game_component]

    def get_objects(self, game_component: GameComponent) -> Tuple[GameObject, ...]:
        if game_component not in self._components:
            raise RuntimeError(f"Component not found: {game_component}")

        return tuple(self._component_objects[game_component])
