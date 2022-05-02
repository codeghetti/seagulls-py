from abc import abstractmethod
from typing import Protocol


class IGameScene(Protocol):
    """
    This class is for X and Y.
    """

    @abstractmethod
    def tick(self) -> None:
        """"""


class IProvideGameScenes(Protocol):

    @abstractmethod
    def get(self) -> IGameScene:
        """"""
