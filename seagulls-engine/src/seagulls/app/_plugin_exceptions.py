from importlib_metadata import EntryPoint


class InvalidPluginError(RuntimeError):
    entry_point: EntryPoint

    def __init__(self, entry_point: EntryPoint):
        super().__init__(f"Invalid plugin entry_point detected: {entry_point}")
        self.entry_point = entry_point
