from abc import abstractmethod
from typing import Protocol


class ISeagullsApplication(Protocol):

    @abstractmethod
    def execute(self) -> None:
        """
        Do your thing.
        """
