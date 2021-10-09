import logging

from seagulls.engine import GameObject, GameScene, GameSceneObjects, Surface

logger = logging.getLogger(__name__)


class StorybookScene(GameScene):
    """
    Scene used to test and demo as much functionality as possible.
    """

    def __init__(self):
        pass

    def start(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def pause(self) -> None:
        pass

    def update(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        pass

    def add_game_object(self, obj: GameObject) -> None:
        pass

    def get_scene_objects(self) -> GameSceneObjects:
        pass
