from abc import abstractmethod, ABC

from ._overwrites import Surface


class GameObject(ABC):

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self, surface: Surface) -> None:
        pass
