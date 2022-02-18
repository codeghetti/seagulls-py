from seagulls.space_shooter import ActiveShipClient


class TestActiveShipClient:

    def test_basics(self):
        active_ship_client = ActiveShipClient("test_ship")

        active_ship_client.get_active_ship()

        active_ship_client.set_active_ship("test_ship")
