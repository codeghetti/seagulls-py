from pygame import Surface

from seagulls.cat_demos.engine.v2.components._component_containers import (
    GameComponentId,
    GameComponentType,
    TypedGameComponentContainer,
)


class SpriteContainer(TypedGameComponentContainer[Surface]):

    _container: TypedGameComponentContainer[Surface]

    def __init__(self, container: TypedGameComponentContainer[Surface]) -> None:
        self._container = container

    def get(self, component_id: GameComponentId[GameComponentType]) -> GameComponentType:
        return self._container.get(GameComponentId(f"sprite::{component_id.name}"))
