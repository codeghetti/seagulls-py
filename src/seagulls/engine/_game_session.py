from abc import ABC, abstractmethod


class IGameSession(ABC):

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def wait_for_completion(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
