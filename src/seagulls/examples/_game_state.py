from seagulls.engine import IGameScene


class GameState:
    active_scene: IGameScene
    game_state_changed: bool = False
