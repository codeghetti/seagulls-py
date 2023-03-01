from abc import abstractmethod
from typing import Any, Dict, Protocol, Tuple

from seagulls.cat_demos.engine.v2.components._identity import EntityType
from seagulls.cat_demos.engine.v2.components._object_components import GameComponentId
from seagulls.cat_demos.engine.v2.components._scene_objects import GameObjectId


class IProvideGameObjectComponent(Protocol[EntityType]):

    @abstractmethod
    def tick(self, game_object: GameObjectId) -> None:
        pass

    @abstractmethod
    def get(self, game_object: GameObjectId) -> EntityType:
        pass


class GameComponentRegistry:

    _components: Dict[GameComponentId[Any], IProvideGameObjectComponent[Any]]

    def __init__(self) -> None:
        self._components = {}

    def register(
        self,
        component: GameComponentId[EntityType],
        provider: IProvideGameObjectComponent[EntityType],
    ) -> None:
        self._components[component] = provider

    def get_ids(self) -> Tuple[GameComponentId[Any]]:
        return tuple(self._components.keys())

    def get_provider(
        self,
        component: GameComponentId[EntityType],
    ) -> IProvideGameObjectComponent[EntityType]:
        return self._components[component]
