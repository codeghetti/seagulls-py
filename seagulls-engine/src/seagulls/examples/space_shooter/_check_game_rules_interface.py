from abc import ABC, abstractmethod


class ICheckGameRules(ABC):

    @abstractmethod
    def check(self) -> None:
        pass
