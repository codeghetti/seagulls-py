from seagulls.app import ISeagullsApplication


def test_basics() -> None:
    # We just need to assert that our interface exists, and we are able to import it.
    assert ISeagullsApplication
