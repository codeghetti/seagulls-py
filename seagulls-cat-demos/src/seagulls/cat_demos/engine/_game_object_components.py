from dataclasses import dataclass

from typing import Generic, TypeVar, Dict, Any, Tuple, List

ComponentType = TypeVar("ComponentType")


@dataclass(frozen=True)
class ComponentId(Generic[ComponentType]):
    key: str


class GameObjectComponents:

    _components: Dict[ComponentId[ComponentType], ComponentType]

    def __init__(self) -> None:
        self._components = {}

    def get_ids(self) -> Tuple[ComponentId[Any], ...]:
        return tuple(self._components.keys())

    def get_component(self, component_id: ComponentId[ComponentType]) -> ComponentType:
        return self._components[component_id]

    def add_component(
            self, component_id: ComponentId[ComponentType], component: ComponentType) -> None:
        if component_id in self._components:
            raise RuntimeError(f"Duplicate component found: {component_id}")

        self._components[component_id] = component
