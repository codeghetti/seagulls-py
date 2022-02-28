# type: ignore
from typing import Any, Dict, Tuple, Type

import pytest

from seagulls.app import (
    ISeagullsApplicationPluginRegistrant,
    SeagullsEntryPointsPluginsClient
)
from seagulls.app._plugin_client import SeagullsEntryPointsPluginSource
from seagulls.app._plugin_exceptions import InvalidPluginError


class FakeRegistrant:
    @staticmethod
    def register_plugins(application: Dict) -> None:
        application["loaded-plugin"] = True


class FakeEntryPoint:
    _group: str
    _result: Any

    def __init__(self, group: str, result: Any):
        self._group = group
        self._result = result

    def load(self) -> Any:
        return self._result


class InvalidEntryPoint:
    pass


class TestSeagullsEntryPointsPluginSource:

    def test_basics(self) -> None:
        expected = tuple([FakeRegistrant])

        def callback(group: str) -> Tuple[Any, ...]:
            return tuple([FakeEntryPoint("example.plugins", FakeRegistrant)])

        # We just ask for the entry points
        ut = SeagullsEntryPointsPluginSource(callback)
        result = ut.entry_points("example.plugins")
        assert result == expected

    def test_plugin_validation(self) -> None:
        invalid_values = [InvalidEntryPoint, False, None, 1, "hello", {}]

        for value in invalid_values:
            def callback(group: str) -> Tuple[Any, ...]:
                return tuple([FakeEntryPoint("example.plugins", value)])

            # We just ask for the entry points
            ut = SeagullsEntryPointsPluginSource(callback)
            with pytest.raises(InvalidPluginError):
                ut.entry_points("example.plugins")


class FakeSource:
    def entry_points(self, group: str) -> Tuple[Type[ISeagullsApplicationPluginRegistrant], ...]:
        return tuple([FakeRegistrant])


class TestSeagullsEntryPointsPluginsClient:
    _ut: SeagullsEntryPointsPluginsClient

    def setup(self) -> None:
        self._ut = SeagullsEntryPointsPluginsClient(
            entrypoint_source=FakeSource(),
            entrypoint_name="example.plugins",
        )

    def test_basics(self) -> None:
        app = {}
        self._ut.register_plugins(app)
        assert app["loaded-plugin"]
