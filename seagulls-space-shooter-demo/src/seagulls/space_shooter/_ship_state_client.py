class ShipStateClient:
    _powered_state: bool

    def __init__(self):
        self._powered_state = False

    def update_state(self, state: bool) -> None:
        self._powered_state = state

    def is_powered_up(self) -> bool:
        return self._powered_state
