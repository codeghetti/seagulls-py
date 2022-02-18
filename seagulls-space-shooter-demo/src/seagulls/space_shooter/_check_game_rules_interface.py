from abc import ABC, abstractmethod


class ICheckGameRules(ABC):

    @abstractmethod
    def check(self) -> None:
        """This should check the game rule to see if it has been met"""
