from seagulls.engine import IGameScene


class WindowScene(IGameScene):
    _active_scene: IGameScene
    _next_scene: IGameScene

    def __init__(self, active_scene: IGameScene, next_scene: IGameScene):
        self._active_scene = active_scene
        self._next_scene = next_scene

    def start(self) -> None:
        self._active_scene.start()

    def should_quit(self) -> bool:
        return self._active_scene.should_quit()

    def tick(self) -> None:
        if self._active_scene.should_switch_scene:
            self._active_scene = self._next_scene
            self._active_scene.start()
        self._active_scene.tick()
