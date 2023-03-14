from typing import Set

from seagulls.cat_demos.engine.v2.components._component_registry import GameComponentId


class GameSceneComponents:

    _scene_components: Set[GameComponentId]

    def __init__(self) -> None:
        self._scene_components = set()

    def enable_components(self, *component: GameComponentId) -> None:
        for c in component:
            self.enable_component(c)

    def enable_component(self, component_id: GameComponentId) -> None:
        self._scene_components.add(component_id)
