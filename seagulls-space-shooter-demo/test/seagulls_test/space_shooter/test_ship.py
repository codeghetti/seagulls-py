from seagulls.space_shooter import Ship


class TestShip:

    def test_basics(self):
        Ship(
            "active_ship_manager",
            "clock",
            "asset_manager",
            "game_controls",
            "fit_to_screen"
        )
