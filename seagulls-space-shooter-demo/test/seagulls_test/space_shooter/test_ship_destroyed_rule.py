from seagulls.space_shooter._ship_destroyed_rule import ShipDestroyedRule


class TestShipDestroyedRule:
    def test_basics(self):
        ShipDestroyedRule("state_client", "asteroid_field", "ship", "fit_to_scree")
