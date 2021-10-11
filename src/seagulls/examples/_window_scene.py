from seagulls.engine import IGameScene


class WindowScene(IGameScene):
    _active_scene: IGameScene
    _first_scene: IGameScene
    _second_scene: IGameScene

    def __init__(self, active_scene: IGameScene, first_scene: IGameScene, second_scene: IGameScene):
        self._active_scene = active_scene
        self._first_scene = first_scene
        self._second_scene = second_scene

    def start(self) -> None:
        self._active_scene.start()

    def should_quit(self) -> bool:
        return self._active_scene.should_quit()

    def tick(self) -> None:
        if self._active_scene.first_should_switch_scene:
            self._active_scene = self._first_scene
            self._active_scene.start()
        if self._active_scene.second_should_switch_scene:
            self._active_scene = self._second_scene
            self._active_scene.start()
        self._active_scene.tick()
