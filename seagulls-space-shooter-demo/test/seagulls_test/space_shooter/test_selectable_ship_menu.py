from seagulls.space_shooter import ShipSelectionMenu, ShipSelectionMenuFactory


class TestShipSelectionMenuFactory:

    def test_get_instance(self):
        test = ShipSelectionMenuFactory(
            "catalog",
            "surface_renderer",
            "game_controls",
            "asset_manager",
            "active_scene_manager",
            "active_ship_manager",
            "background",
            "fit_to_screen"
            )

        assert isinstance(test.get_instance("game_scene"), ShipSelectionMenu)
