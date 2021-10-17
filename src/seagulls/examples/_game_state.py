from typing import Optional

from seagulls.engine import IGameScene


class GameState:
    active_scene: Optional[IGameScene] = None
    game_state_changed: bool = False

