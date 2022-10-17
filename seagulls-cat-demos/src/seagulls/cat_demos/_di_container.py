from functools import lru_cache

from seagulls.seagulls_cli import SeagullsCliApplication

from ._cli_command import GameCliCommand
from ._cli_plugin import CatDemosCliPlugin


class CatDemosDiContainer:
    _application: SeagullsCliApplication

    def __init__(self, application: SeagullsCliApplication):
        self._application = application

    @lru_cache()
    def plugin(self) -> CatDemosCliPlugin:
        return CatDemosCliPlugin(
            application=self._application,
            command=self._command(),
        )

    @lru_cache()
    def _command(self) -> GameCliCommand:
        return GameCliCommand()
