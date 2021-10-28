from abc import ABC, abstractmethod
from typing import Callable

from seagulls.engine import IGameScene


class IProvideActiveScene(ABC):

    @abstractmethod
    def apply(self, callback: Callable[[IGameScene], None]):
        pass


class ISetActiveScene(ABC):

    @abstractmethod
    def set_active_scene(self, scene: IGameScene) -> None:
        pass


class ActiveSceneClient(IProvideActiveScene, ISetActiveScene):

    _active_scene: IGameScene

    def __init__(self, scene: IGameScene):
        self._active_scene = scene

    def apply(self, callback: Callable[[IGameScene], None]):
        callback(self._active_scene)

    def set_active_scene(self, scene: IGameScene) -> None:
        self._active_scene = scene
