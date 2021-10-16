from seagulls.engine import IGameScene


class GameState:
    active_scene: IGameScene = None
    game_state_changed: bool = False

