from seagulls.space_shooter import BlueShip


class FakeFitToScreen:

    def get_actual_surface_width(self) -> float:
        return 900.0


class TestBlueShip:

    def test_basics(self):
        fake_fit_to_screen = FakeFitToScreen()

        ship = BlueShip(fake_fit_to_screen)  # type: ignore

        ship.sprite()

        ship.velocity()

        ship.power()

        ship.display_name()

        ship.offset()
