import sys
from typing import Type

from ._plugin_exceptions import InvalidPluginError

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

from ._plugin_interfaces import (
    ApplicationType,
    ISeagullsApplicationPluginRegistrant,
    ISeagullsPluginClient
)


class SeagullsEntryPointsPluginsClient(ISeagullsPluginClient):

    _entrypoint_name: str

    def __init__(self, entrypoint_name: str):
        self._entrypoint_name = entrypoint_name

    def register_plugins(self, application: ApplicationType) -> None:
        plugins = entry_points(group=self._entrypoint_name)
        for plugin in plugins:
            plugin_ref: Type[ISeagullsApplicationPluginRegistrant] = plugin.load()
            if not issubclass(plugin_ref, ISeagullsApplicationPluginRegistrant):
                raise InvalidPluginError(plugin)

            plugin_ref.register_plugins(application)  # type: ignore
