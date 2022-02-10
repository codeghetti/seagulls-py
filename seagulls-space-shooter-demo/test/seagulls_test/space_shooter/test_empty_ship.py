import pytest

from seagulls.space_shooter._empty_ship import EmptyShip


class TestEmptyShip:

    def test_basics(self):
        ship = EmptyShip()

        with pytest.raises(RuntimeError):
            ship.sprite()

        with pytest.raises(RuntimeError):
            ship.velocity()

        with pytest.raises(RuntimeError):
            ship.power()

        with pytest.raises(RuntimeError):
            ship.display_name()

        with pytest.raises(RuntimeError):
            ship.offset()
