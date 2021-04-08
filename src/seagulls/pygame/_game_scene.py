from abc import ABC, abstractmethod
from typing import List, Tuple

from ._game_object import GameObject

from ._overwrites import Surface


class GameSceneObjects:
    _objects: List[GameObject]

    def __init__(self):
        self._objects = []

    def update(self) -> None:
        for index, obj in enumerate(self._objects):
            if obj.is_destroyed():
                del self._objects[index]

    def add(self, obj: GameObject) -> None:
        self._objects.append(obj)

    def get_objects(self) -> Tuple[GameObject, ...]:
        return tuple(self._objects)

    def count_objects(self) -> int:
        return len(self._objects)

    def clear(self) -> None:
        self._objects = []


class GameScene(ABC):

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass

    @abstractmethod
    def pause(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self, surface: Surface) -> None:
        pass

    @abstractmethod
    def add_game_object(self, obj: GameObject) -> None:
        pass

    @abstractmethod
    def get_scene_objects(self) -> GameSceneObjects:
        pass


class GameSceneManager:
    _active_scene: GameScene

    def load_scene(self, scene: GameScene) -> None:
        self._active_scene = scene

    def start_scene(self) -> None:
        self._active_scene.start()

    def exit_scene(self) -> None:
        self._active_scene.exit()

    def pause_scene(self) -> None:
        self._active_scene.pause()

    def update_scene(self) -> None:
        self._active_scene.update()

    def render_scene(self, surface: Surface) -> None:
        self._active_scene.render(surface)

    def get_scene_objects(self) -> GameSceneObjects:
        return self._active_scene.get_scene_objects()
