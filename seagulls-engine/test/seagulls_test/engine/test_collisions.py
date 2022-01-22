import pytest

from seagulls.engine import CollidableObject, flag_from_string


class TestFunctions:
    def test_basics(self) -> None:
        assert flag_from_string("0001") == 1
        assert flag_from_string("0010") == 2
        assert flag_from_string("0011") == 3

        with pytest.raises(ValueError):
            flag_from_string("00a1")


class TestCollidableObject:

    def test_is_in_mask(self) -> None:
        thing1 = CollidableObject(layer=flag_from_string("00001"), mask=flag_from_string("00010"))
        thing2 = CollidableObject(layer=flag_from_string("00010"), mask=flag_from_string("00100"))
        # Thing 1 is looking for any object in layer "00010"
        assert thing1.is_in_mask(thing2)
        # Thing 2 is looking for any object in layer "00100"
        assert not thing2.is_in_mask(thing1)

    def test_filter_by_mask(self) -> None:
        thing1 = CollidableObject(layer=flag_from_string("00001"), mask=flag_from_string("00011"))
        thing2 = CollidableObject(layer=flag_from_string("00010"), mask=flag_from_string("00100"))
        thing3 = CollidableObject(layer=flag_from_string("00100"), mask=flag_from_string("00101"))

        t1 = tuple([thing1, thing3])
        t2 = tuple([thing1, thing2])
        t3 = tuple([thing2, thing3])

        assert thing1.filter_by_mask(t3) == tuple([thing2])
        assert thing2.filter_by_mask(t1) == tuple([thing3])
        assert thing3.filter_by_mask(t2) == tuple([thing1])
