from typing import Tuple

from seagulls.space_shooter._asteroid_missed_rule import AsteroidMissedRule
from seagulls.space_shooter._shooter_scene_client import ShooterSceneState


class FakeTestObject:
    state: ShooterSceneState
    _num_space_rocks: int

    def __init__(self, num_space_rocks: int):
        self.state = ShooterSceneState.RUNNING
        self._num_space_rocks = num_space_rocks

    def get_asteroid_field_size(self) -> int:
        return self._num_space_rocks

    def get_rock_position_y(self, x: int) -> float:
        return x

    def get_y_boundaries(self) -> Tuple[float, float]:
        return 1.0, 5.0

    def update_state(self, state: ShooterSceneState) -> None:
        self.state = state


class TestAsteroidMissedRule:

    def test_check_rule_triggered(self):
        fake_test_object = FakeTestObject(7)
        client = AsteroidMissedRule(fake_test_object, fake_test_object, fake_test_object)
        client.check()
        assert fake_test_object.state == ShooterSceneState.LOST

    def test_check_rule_not_triggered(self):
        fake_test_object = FakeTestObject(2)
        client = AsteroidMissedRule(fake_test_object, fake_test_object, fake_test_object)
        client.check()
        assert fake_test_object.state == ShooterSceneState.RUNNING
