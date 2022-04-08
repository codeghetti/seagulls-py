from abc import abstractmethod
from typing import Protocol


class IGameScreen(Protocol):

    @abstractmethod
    def refresh(self) -> None:
        """"""


class IProvideGameScreens(Protocol):
    @abstractmethod
    def get(self) -> IGameScreen:
        """"""
