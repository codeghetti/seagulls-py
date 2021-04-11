from abc import abstractmethod, ABC

from ._pyagme import Surface


class GameObject(ABC):

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self, surface: Surface) -> None:
        pass

    @abstractmethod
    def is_destroyed(self) -> bool:
        pass
