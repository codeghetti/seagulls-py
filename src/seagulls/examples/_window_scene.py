from seagulls.engine import IGameScene

from ._active_scene_client import IProvideActiveScene


class WindowScene(IGameScene):
    _active_scene_provider: IProvideActiveScene
    _should_quit: bool

    def __init__(self, active_scene_provider: IProvideActiveScene):
        self._active_scene_provider = active_scene_provider
        self._should_quit = False

    def start(self) -> None:
        self._active_scene_provider.apply(lambda x: x.start())

    def should_quit(self) -> bool:
        return self._should_quit

    def tick(self) -> None:
        self._active_scene_provider.apply(lambda x: x.tick())
        self._active_scene_provider.apply(self._update_quit_flag)

    def _update_quit_flag(self, scene: IGameScene) -> None:
        self._should_quit = scene.should_quit()
