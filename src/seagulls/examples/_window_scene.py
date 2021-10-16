from seagulls.engine import IGameScene
from ._game_state import GameState


class WindowScene(IGameScene):
    _active_scene: IGameScene
    _game_state: GameState

    def __init__(self, active_scene: IGameScene, game_state: GameState):
        self._active_scene = active_scene
        self._game_state = game_state
        self._game_state.active_scene = active_scene

    def start(self) -> None:
        self._active_scene.start()

    def should_quit(self) -> bool:
        return self._active_scene.should_quit()

    def tick(self) -> None:
        if self._game_state.game_state_changed:
            self._update_scene()
            self._active_scene.start()
        self._active_scene.tick()

    def _update_scene(self) -> None:
        self._active_scene = self._game_state.active_scene
        self._game_state.game_state_changed = False
