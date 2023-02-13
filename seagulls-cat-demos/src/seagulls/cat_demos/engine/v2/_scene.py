from abc import abstractmethod

from typing import Any, Dict, Protocol, Set, Tuple

from ._component_registry import GameComponentRegistry, IProvideGameObjectComponent
from seagulls.cat_demos.engine.v2.components._identity import EntityType, GameComponentId, GameObjectId
from ._window import GameWindowClient


class ITick(Protocol):

    @abstractmethod
    def tick(self) -> None:
        pass


class IUpdate(Protocol):
    @abstractmethod
    def update(self, game_object: GameObjectId) -> None:
        pass


class GameObjectComponents:

    _component_registry: GameComponentRegistry
    _game_object: GameObjectId
    _components: Set[GameComponentId[Any]]

    def __init__(self, component_registry: GameComponentRegistry, game_object: GameObjectId) -> None:
        self._component_registry = component_registry
        self._game_object = game_object
        self._components = set()

    def get_all(self) -> Tuple[GameComponentId[Any], ...]:
        return tuple(self._components)

    def get(self, component: GameComponentId[EntityType]) -> EntityType:
        return self._component_registry.get_provider(component).get(self._game_object)

    def add(self, component: GameComponentId[Any]) -> None:
        self._components.add(component)

    def remove(self, component: GameComponentId[Any]) -> None:
        self._components.remove(component)


class GameSceneObjects(ITick):

    _window: GameWindowClient
    _objects: Set[GameObjectId]
    _object_components: Dict[GameObjectId, GameObjectComponents]
    _components: GameComponentRegistry

    def __init__(self, window: GameWindowClient) -> None:
        self._window = window
        self._objects = set()
        self._components = GameComponentRegistry()
        self._object_components = {}

    def create_object(self, game_object: GameObjectId) -> None:
        """
        Add a GameObject to the scene.

        The GameObject will not have any components attached to it so make sure this is done before
        the end of the frame. Components can be attached with the attach_component() method.
        """
        if game_object in self._objects:
            raise RuntimeError(f"Duplicate object found: {game_object}")

        self._objects.add(game_object)
        self._object_components[game_object] = GameObjectComponents(
            component_registry=self._components,
            game_object=game_object,
        )

    def create_component(
        self,
        component: GameComponentId[EntityType],
        provider: IProvideGameObjectComponent[EntityType],
    ) -> None:
        """
        Configure a GameComponent for the scene.

        Before a component can be attached to a game object.
        """
        self._components.register(component, provider)

    def attach_component(
        self,
        game_object: GameObjectId,
        component: GameComponentId[Any],
    ) -> None:
        if game_object not in self._objects:
            raise RuntimeError(f"Object not found: {game_object}")

        self._object_components[game_object].add(component)

    def get_object_components(self, game_object: GameObjectId) -> GameObjectComponents:
        return self._object_components[game_object]

    def tick(self) -> None:
        for component_id in self._components.get_ids():
            for game_object, components in self._object_components.items():
                if component_id in components.get_all():
                    self._components.get_provider(component_id).tick(game_object)
        # for component, handler in self._components.items():
        #     handler.tick()
        #     for game_object in self._component_objects.get(component, set()):
        #         cast(IUpdate, handler).update(game_object)
        # self._window.commit()
