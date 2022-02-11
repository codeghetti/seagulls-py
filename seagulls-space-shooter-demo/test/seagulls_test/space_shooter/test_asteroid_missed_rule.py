from seagulls.space_shooter._asteroid_missed_rule import AsteroidMissedRule


class TestAsteroidMissedRule:

    def test_basics(self):
        AsteroidMissedRule(
            "state_client",
            "asteroid_field",
            "fit_to_screen"
        )
