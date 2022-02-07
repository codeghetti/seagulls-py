from importlib_metadata import EntryPoint

from ._plugin_interfaces import ISeagullsApplicationPlugin


class DuplicatePluginError(RuntimeError):
    plugin: ISeagullsApplicationPlugin

    def __init__(self, plugin: ISeagullsApplicationPlugin):
        super().__init__(f"Duplicate plugin registration detected: {type(plugin)}")
        self.plugin = plugin


class InvalidPluginError(RuntimeError):
    entry_point: EntryPoint

    def __init__(self, entry_point: EntryPoint):
        super().__init__(f"Invalid plugin entry_point detected: {entry_point}")
        self.entry_point = entry_point
