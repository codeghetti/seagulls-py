from seagulls.space_shooter._ship_button import ShipButton


class TestShipButton:

    def test_basics(self):
        ShipButton(
            "ship",
            "scene",
            "asset_manager",
            "game_controls",
            "active_scene_manager",
            "active_ship_manager",
            "fit_to_screen"
        )
