from typing import Tuple, Type

from ._plugin_exceptions import InvalidPluginError
from ._plugin_interfaces import (
    ApplicationType,
    EntryPointsCallback,
    ILocatePluginRegistrants,
    ISeagullsApplicationPluginRegistrant,
    ISeagullsPluginClient
)


class SeagullsEntryPointsPluginSource(ILocatePluginRegistrants):

    _entry_points_callable: EntryPointsCallback

    def __init__(self, entry_points_callable: EntryPointsCallback):
        self._entry_points_callable = entry_points_callable

    def entry_points(self, group: str) -> Tuple[Type[ISeagullsApplicationPluginRegistrant], ...]:
        results = []
        for plugin in self._entry_points_callable(group=group):
            plugin_ref: Type[ISeagullsApplicationPluginRegistrant] = plugin.load()
            try:
                if not issubclass(plugin_ref, ISeagullsApplicationPluginRegistrant):
                    raise InvalidPluginError(plugin)
            except TypeError as e:
                raise InvalidPluginError(plugin) from e

            results.append(plugin_ref)

        return tuple(results)


class SeagullsEntryPointsPluginsClient(ISeagullsPluginClient):

    _entrypoint_source: ILocatePluginRegistrants
    _entrypoint_name: str

    def __init__(self, entrypoint_source: ILocatePluginRegistrants, entrypoint_name: str):
        self._entrypoint_source = entrypoint_source
        self._entrypoint_name = entrypoint_name

    def register_plugins(self, application: ApplicationType) -> None:
        for plugin_ref in self._entrypoint_source.entry_points(self._entrypoint_name):
            # Anyone know why mypy fails on this type check?
            plugin_ref.register_plugins(application)  # type: ignore
