from ._check_game_rules_interface import ICheckGameRules
from ._score_tracker import ScoreTracker
from ._ship_state_client import ShipStateClient


class ShipPoweredUpRule(ICheckGameRules):
    _score_tracker: ScoreTracker
    _state_client: ShipStateClient

    def __init__(
            self,
            state_client: ShipStateClient,
            score_tracker: ScoreTracker):
        self._score_tracker = score_tracker
        self._state_client = state_client

    def check(self) -> None:
        if not self._state_client.is_powered_up() and self._score_threshold_check():
            self._state_client.update_state(True)

    def _score_threshold_check(self) -> bool:
        return self._score_tracker.get_score() >= 20
