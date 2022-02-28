from seagulls.cli import (
    CliRequest,
    CliRequestRegistrationEvent,
    RequestEnvironment
)


class TestRequestEnvironment:
    def test_basics(self) -> None:
        env = RequestEnvironment(tuple([("foo", "bar")]))
        assert env.get("foo") == "bar"
        assert env.get("miss") is None
        assert env.get("miss", "default") == "default"
        assert env.as_dict() == {"foo": "bar"}


class TestCliRequestRegistrationEvent:
    def test_nothing(self) -> None:
        assert CliRequestRegistrationEvent


class TestCliRequest:
    def test_nothing(self) -> None:
        assert CliRequest
