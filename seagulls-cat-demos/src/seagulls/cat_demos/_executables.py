from abc import abstractmethod

from typing import Protocol


class IExecutable(Protocol):
    @abstractmethod
    def execute(self) -> None:
        pass


class ITick(Protocol):
    @abstractmethod
    def tick(self) -> None:
        pass
