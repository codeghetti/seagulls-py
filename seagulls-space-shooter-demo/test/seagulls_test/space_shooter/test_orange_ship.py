from seagulls.space_shooter import OrangeShip


class TestOrangeShip:

    def test_basics(self):
        ship = OrangeShip()

        ship.sprite()

        ship.velocity()

        ship.power()

        ship.display_name()

        ship.offset()
