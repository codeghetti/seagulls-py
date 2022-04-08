from abc import abstractmethod
from typing import Protocol, Tuple


class RenderableComponent(Protocol):
    @abstractmethod
    def render(self) -> None:
        """"""


class IProvideRenderables(Protocol):

    @abstractmethod
    def get(self) -> Tuple[RenderableComponent, ...]:
        """"""
